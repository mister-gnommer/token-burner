#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

import jsonschema

from evidence_pipeline import SCHEMA_DIR, TASK_ROOT, author_key, load_records

SCORER_VERSION = "observed-coendorsement-v1"
FAN_CLASSES = {"same_user_rating_overlap", "same_user_coendorsement", "fan_recommendation", "fan_comparison"}
SUPPORT_CLASSES = {"same_user_rating_overlap", "same_user_coendorsement"}
MIN_CONFIDENCE = 0.75


def check_schema(name, record):
    schema = json.loads((SCHEMA_DIR / name).read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker()).validate(record)


def load_evidence(manifest_paths, data_root, synthetic):
    evidence, ignored, seen_runs, seen_records = [], [], set(), set()
    for path in manifest_paths:
        manifest = json.loads(path.read_text(encoding="utf-8"))
        check_schema("run-manifest.schema.json", manifest)
        run_id = manifest["run_id"]
        if run_id in seen_runs:
            raise ValueError(f"duplicate run: {run_id}")
        seen_runs.add(run_id)
        if manifest["stage"] != "batch" or manifest["status"] != "completed":
            ignored.append({"run_id": run_id, "reason": "requires a completed batch; calibration is excluded"})
            continue
        if bool(re.match(r"^\d{8}-synthetic-", run_id)) != synthetic:
            raise ValueError("synthetic and production inputs must be rendered separately")
        candidates = {}
        for _, candidate in load_records(data_root / manifest["paths"]["source_candidates"]):
            check_schema("source-candidate.schema.json", candidate)
            if candidate["candidate_id"] in candidates or candidate["run_id"] != run_id:
                raise ValueError("duplicate candidate or mismatched candidate run")
            if candidate["author_hint"] is not None and candidate["author_key"] != author_key(candidate["site"], candidate["author_hint"]):
                raise ValueError("candidate author key does not match its source-local hint")
            if candidate["collector"] != manifest["workers"]["collector"]:
                raise ValueError("collector provenance differs from its manifest")
            candidates[candidate["candidate_id"]] = candidate
        records = [record for _, record in load_records(data_root / manifest["paths"]["evidence"])]
        seen_candidates = set()
        for record in records:
            check_schema("evidence-v2.schema.json", record)
            candidate = candidates.get(record["candidate_id"])
            if candidate is None or record["extraction"]["run_id"] != run_id:
                raise ValueError("evidence has no matching source candidate/run")
            if any(record["extraction"][key] != value for key, value in manifest["workers"]["extractor"].items()):
                raise ValueError("extractor provenance differs from its manifest")
            if record["id"] in seen_records or record["candidate_id"] in seen_candidates:
                raise ValueError("duplicate evidence or candidate extraction")
            seen_records.add(record["id"])
            seen_candidates.add(record["candidate_id"])
            if record["excerpt"] != candidate["excerpt"] or record["language"] != candidate["language"] or record["source"] != {key: candidate[key] for key in record["source"]}:
                raise ValueError("evidence differs from its source candidate")
            if record["review"]["status"] == "accepted" and not record["review"]["reviewer"]:
                raise ValueError("accepted evidence has no reviewer")
        counts = manifest["counts"]
        if counts["source_candidates"] != len(candidates) or counts["extracted"] != len(records) or any(counts[status] != sum(r["review"]["status"] == status for r in records) for status in ["accepted", "uncertain", "rejected"]):
            raise ValueError("manifest counts differ from saved artifacts")
        evidence.extend(records)
    return evidence, ignored


def aggregate(performers, evidence, updated_at):
    ids = {p["id"] for p in performers}
    if len(ids) != len(performers):
        raise ValueError("duplicate performer ID")
    likes = defaultdict(set)
    support, contradictions = defaultdict(list), defaultdict(list)
    deferred = []
    seen = set()
    for record in sorted(evidence, key=lambda r: r["id"]):
        if record["id"] in seen:
            raise ValueError("duplicate evidence ID")
        seen.add(record["id"])
        mentions = defaultdict(list)
        for mention in record["mentions"]:
            performer_id = mention["performer_id"]
            if performer_id is not None and performer_id not in ids:
                raise ValueError(f"unknown performer: {performer_id}")
            mentions[performer_id].append(mention)
        reason = None
        if record["review"]["status"] != "accepted":
            reason = "review is not accepted"
        elif record["evidence_class"] not in FAN_CLASSES:
            reason = "separate style layer"
        elif not record["source"]["author_key"]:
            reason = "no source-scoped fan key"
        elif None in mentions or any(len({m["sentiment"] for m in group}) != 1 or group[0]["sentiment"] in {"mixed", "unclear"} for group in mentions.values()):
            reason = "unresolved or qualified interpretation needs pair-specific review"
        elif record["extraction"]["confidence"] < MIN_CONFIDENCE or any(m["confidence"] < MIN_CONFIDENCE for group in mentions.values() for m in group):
            reason = "below heuristic confidence threshold"
        if reason:
            deferred.append({"id": record["id"], "reason": reason})
            continue
        fan = (record["source"]["site"].strip().casefold(), record["source"]["author_key"])
        positive = sorted(pid for pid, group in mentions.items() if group[0]["sentiment"] == "positive")
        negative = sorted(pid for pid, group in mentions.items() if group[0]["sentiment"] == "negative")
        for pid in positive:
            likes[pid].add(fan)
        if record["evidence_class"] in SUPPORT_CLASSES:
            for pair in combinations(positive, 2):
                confidence = min(record["extraction"]["confidence"], *(m["confidence"] for pid in pair for m in mentions[pid]))
                support[pair].append((record, fan, confidence))
        for a in positive:
            for b in negative:
                contradictions[tuple(sorted((a, b)))].append(record)
    relations = []
    for pair in sorted(support.keys() | contradictions.keys()):
        rows = support[pair]
        fans = {}
        for record, fan, confidence in rows:
            fans[fan] = max(fans.get(fan, 0), confidence)
        opposed = contradictions[pair]
        union = likes[pair[0]] | likes[pair[1]]
        score = len(fans) / len(union) if union else 0
        accepted = len(fans) >= 2 and not opposed
        relation = {
            "schema_version": 1, "id": "rel_" + "__".join(pair), "pair": list(pair),
            "relation_type": "fan_overlap", "status": "accepted" if accepted else "uncertain",
            "support_evidence_ids": sorted({r["id"] for r, _, _ in rows}),
            "contradictory_evidence_ids": sorted({r["id"] for r in opposed}),
            "independent_source_count": len({(r["source"]["site"], r["source"]["url"]) for r, _, _ in rows}),
            "independent_fan_count": len(fans), "score": round(score, 6),
            "confidence": round(sum(fans.values()) / len(fans), 6) if fans else 0,
            "scorer_version": SCORER_VERSION,
            "explanation": f"{len(fans)} source-scoped fans explicitly co-endorse this pair; {len(union)} observed fans endorse either performer. {len(opposed)} opposing preference records. " + ("Provisional observed overlap." if accepted else "Insufficient independent support or opposing preferences; no visible edge."),
            "updated_at": updated_at,
        }
        check_schema("relation-candidate.schema.json", relation)
        relations.append(relation)
    return relations, deferred, {pid: len(likes[pid]) for pid in sorted(ids)}


def d2_source(graph, max_degree=3):
    quote = lambda value: json.dumps(value, ensure_ascii=False)
    nodes = {node["id"]: f"n{index}" for index, node in enumerate(graph["nodes"])}
    label = "SYNTHETIC FIXTURE — no real fan findings" if graph["synthetic"] else "Provisional fan-preference evidence"
    legend = label + "\nEdge width = observed overlap; labels show fans / confidence.\nConfidence is a model judgment, not a probability.\nLayout distance has no similarity meaning. Missing edges mean insufficient evidence."
    lines = [f"diagram: {quote(legend)} {{", "direction: down"]
    for node in graph["nodes"]:
        lines.extend([f'{nodes[node["id"]]}: {{', f'  label: {quote(node["name"] + chr(10) + str(node["observed_fans"]) + " observed fans")}', '}'])
    degrees = defaultdict(int)
    for relation in sorted(graph["relations"], key=lambda r: (-r["score"], r["id"])):
        if relation["status"] != "accepted" or any(degrees[pid] >= max_degree for pid in relation["pair"]):
            continue
        a, b = relation["pair"]
        for pid in (a, b):
            degrees[pid] += 1
        label = f'{relation["independent_fan_count"]} fans / {relation["confidence"]:.0%} confidence'
        citation_text = relation["explanation"] + " Sources: " + " ".join(graph["evidence_sources"][rid] for rid in relation["support_evidence_ids"])
        lines.extend([f'{nodes[a]} -- {nodes[b]}: {quote(label)} {{', f'  style.stroke-width: {1 + round(5 * relation["score"])}', f'  tooltip: {quote(citation_text)}', '}'])
    lines.append("}")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Build a conservative fan graph and editable D2 snapshot")
    parser.add_argument("--manifest", type=Path, action="append", required=True)
    parser.add_argument("--ranking", type=Path, default=TASK_ROOT / "data/standupers.json")
    parser.add_argument("--data-root", type=Path, default=TASK_ROOT)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--synthetic", action="store_true")
    parser.add_argument("--render", action="store_true")
    args = parser.parse_args()
    try:
        ranking = json.loads(args.ranking.read_text(encoding="utf-8"))
        if not args.synthetic and args.ranking.resolve() != (TASK_ROOT / "data/standupers.json").resolve():
            raise ValueError("production graphs require the frozen ranking")
        evidence, ignored = load_evidence(args.manifest, args.data_root, args.synthetic)
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        relations, deferred, coverage = aggregate(ranking["performers"], evidence, now)
        graph = {"schema_version": 1, "synthetic": args.synthetic, "scorer_version": SCORER_VERSION, "updated_at": now,
                 "input_manifests": [str(path) for path in args.manifest],
                 "renderer": {"name": "d2", "layout": "elk", "sketch": True, "max_degree": 3},
                 "nodes": [{"id": p["id"], "name": p["name"], "observed_fans": coverage[p["id"]]} for p in sorted(ranking["performers"], key=lambda p: p["id"])],
                 "relations": relations, "deferred_evidence": deferred, "ignored_runs": ignored,
                 "evidence_sources": {r["id"]: r["source"]["url"] for r in evidence}}
        args.output.mkdir(parents=True, exist_ok=True)
        (args.output / "graph.json").write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (args.output / "graph.d2").write_text(d2_source(graph), encoding="utf-8")
        if args.render:
            subprocess.run(["d2", "--sketch", "--layout", "elk", str(args.output / "graph.d2"), str(args.output / "graph.svg")], check=True)
            subprocess.run(["rsvg-convert", "-z", "2", str(args.output / "graph.svg"), "-o", str(args.output / "graph.png")], check=True)
        print(f"Saved {len(relations)} relations ({sum(r['status'] == 'accepted' for r in relations)} visible candidates) to {args.output}")
        return 0
    except (OSError, ValueError, jsonschema.ValidationError, subprocess.CalledProcessError) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
