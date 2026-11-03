"""Render graph.json as a self-contained interactive force-directed HTML page.

graph_pipeline.py calls write_page on every build; the CLI re-renders an existing graph.json.

Presentation only: reads existing graph, ranking, manifest and evidence files; never rescores.
"""

import argparse
import base64
import html
import json
from io import BytesIO
from pathlib import Path

from PIL import Image

TASK_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = Path(__file__).with_name("interactive_template.html")
D3 = Path(__file__).with_name("vendor") / "d3-7.9.0.min.js"
AVATAR_PX = 128


def edge_kind(relation):
    if relation["contradictory_evidence_ids"] or not relation["support_evidence_ids"]:
        return "contested"
    return "accepted" if relation["status"] == "accepted" else "provisional"


def supported_dispute(relation):
    return bool(relation["contradictory_evidence_ids"] and relation["support_evidence_ids"]
                and relation["independent_fan_count"] >= 2)


def avatar_data_uri(path):
    if path.suffix == ".svg":
        return "data:image/svg+xml;base64," + base64.b64encode(path.read_bytes()).decode()
    # Re-encode as small JPEGs: embedded PNGs would make the page several MB.
    with Image.open(path) as image:
        image = image.convert("RGB").resize((AVATAR_PX, AVATAR_PX), Image.LANCZOS)
        buffer = BytesIO()
        image.save(buffer, "JPEG", quality=82, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buffer.getvalue()).decode()


def load_evidence(graph, repo_root, task_root):
    records = []
    for manifest_path in graph["input_manifests"]:
        manifest = json.loads((repo_root / manifest_path).read_text())
        lines = (task_root / manifest["paths"]["evidence"]).read_text().splitlines()
        records.extend(json.loads(line) for line in lines if line.strip())
    return records


def evidence_view(record, pair):
    sentiments = {m["performer_id"]: m["sentiment"] for m in record["mentions"] if m.get("performer_id") in pair}
    return {
        "id": record["id"],
        "class": record["evidence_class"].replace("_", " "),
        "site": record["source"]["site"],
        "url": record["source"]["url"],
        "published_at": record["source"].get("published_at"),
        "excerpt": record["excerpt"],
        "sentiments": sentiments,
    }


def build_payload(graph, ranking, evidence_records):
    evidence = {record["id"]: record for record in evidence_records}
    performers = {p["id"]: p for p in ranking["performers"]}
    relations = []
    for relation in graph["relations"]:
        pair = relation["pair"]
        relations.append({
            "source": pair[0],
            "target": pair[1],
            "kind": edge_kind(relation),
            "supported_dispute": supported_dispute(relation),
            "score": relation["score"],
            "confidence": relation["confidence"],
            "fans": relation["independent_fan_count"],
            "explanation": relation["explanation"],
            "support": [evidence_view(evidence[i], pair) for i in relation["support_evidence_ids"] if i in evidence],
            "opposing": [evidence_view(evidence[i], pair) for i in relation["contradictory_evidence_ids"] if i in evidence],
        })
    nodes = []
    for node in graph["nodes"]:
        performer = performers.get(node["id"], {})
        nodes.append({
            "id": node["id"],
            "name": node["name"],
            "rank": performer.get("rank"),
            "profile": performer.get("profile_url"),
            "fans": node["observed_fans"],
            "researched": performer.get("status") == "completed",
            "photo": node["avatar"]["status"] == "photo",
            "avatar": node["avatar"]["path"],
        })
    strict_nodes = {pid for r in relations if r["kind"] != "contested" for pid in [r["source"], r["target"]]}
    displayed_nodes = strict_nodes | {pid for r in relations if r["supported_dispute"] for pid in [r["source"], r["target"]]}
    coverage = {"strict_linked_nodes": len(strict_nodes), "linked_nodes_including_disputed": len(displayed_nodes),
                "disputed_links": sum(r["supported_dispute"] for r in relations)}
    return {"updated_at": graph["updated_at"], "scorer": graph["scorer_version"], "nodes": nodes, "relations": relations,
            "coverage": coverage}


def embed_avatars(payload, graph_dir):
    cache = {}
    for node in payload["nodes"]:
        path = graph_dir / node["avatar"]
        if not path.is_file():
            path = TASK_ROOT / "graph" / "assets" / "laughing-person.svg"
        if path not in cache:
            cache[path] = avatar_data_uri(path)
        node["avatar"] = cache[path]


def write_page(graph, ranking, evidence_records, graph_dir, output):
    payload = build_payload(graph, ranking, evidence_records)
    embed_avatars(payload, graph_dir)
    # "</" must not appear inside the inline <script>; excerpts are untrusted text.
    data = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
    page = (TEMPLATE.read_text()
            .replace("/*__D3__*/", D3.read_text())
            .replace("/*__DATA__*/null", data)
            .replace("__TITLE__", html.escape(f"Stand-up fan graph · {graph['updated_at'][:10]}")))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(page, encoding="utf-8")
    return payload


def render(graph_path, output, data_root):
    graph = json.loads(graph_path.read_text())
    ranking = json.loads((data_root / "data" / "standupers.json").read_text())
    evidence = load_evidence(graph, data_root.parents[1], data_root)
    return write_page(graph, ranking, evidence, graph_path.parent, output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph", type=Path, required=True, help="graph.json produced by graph_pipeline.py")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--data-root", type=Path, default=TASK_ROOT, help="task directory holding data/, evidence/ and reports/")
    args = parser.parse_args()
    payload = render(args.graph, args.output, args.data_root.resolve())
    kinds = [r["kind"] for r in payload["relations"]]
    print(f"{args.output}: {len(payload['nodes'])} nodes, "
          f"{kinds.count('accepted')} accepted / {kinds.count('provisional')} provisional / {kinds.count('contested')} contested")


if __name__ == "__main__":
    main()
