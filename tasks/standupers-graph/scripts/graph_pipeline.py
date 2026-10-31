#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
import sys
import textwrap
from collections import defaultdict
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

import jsonschema

from evidence_pipeline import SCHEMA_DIR, TASK_ROOT, author_key, load_records
from avatars import prepare_avatar

SCORER_VERSION = "observed-coendorsement-v2"
FAN_CLASSES = {"same_user_rating_overlap", "same_user_coendorsement", "fan_recommendation", "fan_comparison"}
SUPPORT_CLASSES = {"same_user_rating_overlap", "same_user_coendorsement"}
MIN_CONFIDENCE = 0.75


def check_schema(name, record):
    schema = json.loads((SCHEMA_DIR / name).read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker()).validate(record)


def load_evidence(manifest_paths, data_root, synthetic):
    evidence, ignored, seen_runs, seen_records = [], [], set(), set()
    seen_posts = set()
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
            check_schema("source-candidate-v2.schema.json" if candidate["schema_version"] == 2 else "source-candidate.schema.json", candidate)
            if candidate["candidate_id"] in candidates or candidate["run_id"] != run_id:
                raise ValueError("duplicate candidate or mismatched candidate run")
            if candidate["author_hint"] is not None and candidate["author_key"] != author_key(candidate["site"], candidate["author_hint"]):
                raise ValueError("candidate author key does not match its source-local hint")
            if candidate["collector"] != manifest["workers"]["collector"]:
                raise ValueError("collector provenance differs from its manifest")
            post = (candidate["site"], candidate["author_key"], candidate["excerpt"])
            if post in seen_posts:
                raise ValueError("duplicate source post; use a replacement run without its original")
            seen_posts.add(post)
            candidates[candidate["candidate_id"]] = candidate
        records = [record for _, record in load_records(data_root / manifest["paths"]["evidence"])]
        seen_candidates = set()
        for record in records:
            check_schema("evidence-v3.schema.json" if record["schema_version"] == 3 else "evidence-v2.schema.json", record)
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
            if record.get("context", []) != candidate.get("context", []):
                raise ValueError("evidence context differs from its source candidate")
            for mention in record["mentions"]:
                if record["schema_version"] == 3 and mention["surface_form"] not in record["excerpt"]:
                    raise ValueError("mention surface is not verbatim")
                if record["schema_version"] == 3:
                    quote = mention["preference_quote"]
                    if (mention["preference"] != "unknown" and (not quote or quote not in record["excerpt"])) or (mention["preference"] == "unknown" and quote is not None):
                        raise ValueError("preference quote is missing, non-verbatim or attached to unknown preference")
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
        elif record["schema_version"] < 3 and (None in mentions or any(len({m["sentiment"] for m in group}) != 1 or group[0]["sentiment"] in {"mixed", "unclear"} for group in mentions.values())):
            reason = "unresolved or qualified interpretation needs pair-specific review"
        elif record["extraction"]["confidence"] < MIN_CONFIDENCE or (record["schema_version"] < 3 and any(m["confidence"] < MIN_CONFIDENCE for group in mentions.values() for m in group)):
            reason = "below heuristic confidence threshold"
        if reason:
            deferred.append({"id": record["id"], "reason": reason})
            continue
        fan = (record["source"]["site"].strip().casefold(), record["source"]["author_key"])
        if record["schema_version"] == 3:
            eligible = {}
            for pid, group in mentions.items():
                preferences = {m["preference"] for m in group}
                if pid is not None and len(preferences) == 1 and all(m["confidence"] >= MIN_CONFIDENCE for m in group):
                    eligible[pid] = group[0]["preference"]
                else:
                    deferred.append({"id": record["id"], "performer_id": pid, "reason": "mention identity, preference or confidence unresolved"})
            positive = sorted(pid for pid, value in eligible.items() if value == "positive")
            negative = sorted(pid for pid, value in eligible.items() if value == "negative")
        else:
            positive = sorted(pid for pid, group in mentions.items() if group[0]["sentiment"] == "positive")
            negative = sorted(pid for pid, group in mentions.items() if group[0]["sentiment"] == "negative")
        for pid in positive:
            likes[pid].add(fan)
        if record["schema_version"] == 3 or record["evidence_class"] in SUPPORT_CLASSES:
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
            "explanation": f"{len(fans)} source-scoped fans explicitly co-endorse this pair; {len(union)} observed fans endorse either performer. {len(opposed)} opposing preference records. " + ("Provisional observed overlap." if accepted else "Insufficient independent support or opposing preferences; eligible uncontested one-fan pairs may be shown as provisional."),
            "updated_at": updated_at,
        }
        check_schema("relation-candidate.schema.json", relation)
        relations.append(relation)
    return relations, deferred, {pid: len(likes[pid]) for pid in sorted(ids)}


def displayable(relation):
    return relation["status"] == "accepted" or (relation["status"] == "uncertain" and relation["independent_fan_count"] == 1 and not relation["contradictory_evidence_ids"])


def d2_source(graph, max_degree=3):
    quote = lambda value: json.dumps(value, ensure_ascii=False)
    nodes = {node["id"]: f"n{index}" for index, node in enumerate(graph["nodes"])}
    visible = set(graph.get("visible_node_ids", nodes))
    label = "SYNTHETIC FIXTURE — no real fan findings" if graph["synthetic"] else "Provisional fan-preference evidence"
    legend = label + "\nSolid = 2+ fans; dashed = PROVISIONAL (1 fan).\nEdge width = observed overlap; labels show fan count / confidence.\nCounts include scoring-eligible statements only.\nConfidence is a model judgment, not a probability.\nLayout distance has no similarity meaning. Missing edges mean insufficient evidence."
    lines = [f"diagram: {quote(legend)} {{", "direction: down"]
    if visible and not any(displayable(r) and set(r["pair"]) <= visible for r in graph["relations"]):
        lines.append(f"grid-columns: {min(5, len(visible))}")
    for node in graph["nodes"]:
        if node["id"] not in visible:
            continue
        name = textwrap.fill(node["name"], width=20, break_long_words=False, break_on_hyphens=False)
        lines.extend([f'{nodes[node["id"]]}: {{', f'  label: {quote(name + chr(10) + str(node["observed_fans"]) + " scored fans")}'])
        if node.get("avatar"):
            lines.extend([f'  icon: {quote("./" + node["avatar"]["path"])}', '  shape: image', '  label.near: outside-bottom-center', '  width: 128', '  height: 128'])
        lines.append('}')
    degrees = defaultdict(int)
    for relation in sorted(graph["relations"], key=lambda r: (r["status"] != "accepted", -r["score"], r["id"])):
        if not displayable(relation) or not set(relation["pair"]) <= visible or any(degrees[pid] >= max_degree for pid in relation["pair"]):
            continue
        a, b = relation["pair"]
        for pid in (a, b):
            degrees[pid] += 1
        fan_count = relation["independent_fan_count"]
        label = f'{fan_count} {"fan" if fan_count == 1 else "fans"} / {relation["confidence"]:.0%}'
        citation_text = relation["explanation"] + " Sources: " + " ".join(graph["evidence_sources"][rid] for rid in relation["support_evidence_ids"])
        lines.extend([f'{nodes[a]} -- {nodes[b]}: {quote(label)} {{', f'  style.stroke-width: {1 + round(5 * relation["score"])}', '  style.font-size: 12', f'  tooltip: {quote(citation_text)}'])
        if relation["status"] != "accepted":
            lines.extend(["  style.stroke-dash: 5", '  style.stroke: "#946200"'])
        lines.append("}")
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
    parser.add_argument("--batch-view", type=int, choices=range(1, 11), help="Show batches up to this number plus supported neighbors; retain all nodes in JSON")
    args = parser.parse_args()
    try:
        ranking = json.loads(args.ranking.read_text(encoding="utf-8"))
        if not args.synthetic and args.ranking.resolve() != (TASK_ROOT / "data/standupers.json").resolve():
            raise ValueError("production graphs require the frozen ranking")
        evidence, ignored = load_evidence(args.manifest, args.data_root, args.synthetic)
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        relations, deferred, coverage = aggregate(ranking["performers"], evidence, now)
        visible = {p["id"] for p in ranking["performers"] if args.batch_view is None or p.get("batch", 1) <= args.batch_view}
        visible.update(pid for relation in relations if displayable(relation) for pid in relation["pair"])
        graph = {"schema_version": 1, "synthetic": args.synthetic, "scorer_version": SCORER_VERSION, "updated_at": now,
                 "input_manifests": [str(path) for path in args.manifest],
                 "renderer": {"name": "d2", "layout": "elk", "sketch": True, "max_degree": 3, "provisional_edges": "one fan, no opposing records"},
                 "visible_node_ids": sorted(visible),
                 "nodes": [{"id": p["id"], "name": p["name"], "observed_fans": coverage[p["id"]],
                            "avatar": prepare_avatar(p, args.output, fetch=args.render and not args.synthetic and p["id"] in visible)} for p in sorted(ranking["performers"], key=lambda p: p["id"])],
                 "relations": relations, "deferred_evidence": deferred, "ignored_runs": ignored,
                 "evidence_sources": {r["id"]: r["source"]["url"] for r in evidence}}
        args.output.mkdir(parents=True, exist_ok=True)
        (args.output / "graph.json").write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (args.output / "graph.d2").write_text(d2_source(graph), encoding="utf-8")
        if args.render:
            subprocess.run(["d2", "--sketch", "--layout", "elk", str(args.output / "graph.d2"), str(args.output / "graph.svg")], check=True)
            subprocess.run(["rsvg-convert", "-z", "2", str(args.output / "graph.svg"), "-o", str(args.output / "graph.png")], check=True)
        print(f"Saved {len(relations)} relations ({sum(r['status'] == 'accepted' for r in relations)} accepted, {sum(displayable(r) and r['status'] != 'accepted' for r in relations)} provisional candidates) to {args.output}")
        return 0
    except (OSError, ValueError, jsonschema.ValidationError, subprocess.CalledProcessError) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
