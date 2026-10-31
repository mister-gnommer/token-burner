import json
import tempfile
import unittest
from pathlib import Path

from render_interactive import edge_kind, render


def relation(status, support, opposing):
    return {"pair": ["lorem", "ipsum"], "status": status, "support_evidence_ids": support, "contradictory_evidence_ids": opposing,
            "score": 0.5, "confidence": 0.9, "independent_fan_count": len(support), "explanation": "Lorem."}


class InteractiveRenderTests(unittest.TestCase):
    def test_opposing_evidence_never_attracts_even_when_accepted(self):
        assert edge_kind(relation("accepted", ["ev_1", "ev_2"], [])) == "accepted"
        assert edge_kind(relation("uncertain", ["ev_1"], [])) == "provisional"
        assert edge_kind(relation("accepted", ["ev_1", "ev_2"], ["ev_3"])) == "contested"
        assert edge_kind(relation("uncertain", [], ["ev_3"])) == "contested"

    def test_untrusted_excerpt_cannot_close_inline_script(self):
        with tempfile.TemporaryDirectory() as directory:
            task = Path(directory) / "tasks" / "lorem"
            (task / "data").mkdir(parents=True)
            (task / "data" / "standupers.json").write_text(json.dumps({"performers": [{"id": "lorem", "rank": 1, "status": "completed"}]}))
            evidence = {"id": "ev_1", "evidence_class": "same_user_coendorsement", "excerpt": "Lorem </script><script>alert(1)</script>",
                        "source": {"site": "example.invalid", "url": "https://example.invalid/1"}, "mentions": []}
            (task / "evidence.jsonl").write_text(json.dumps(evidence) + "\n")
            (task / "manifest.json").write_text(json.dumps({"paths": {"evidence": "evidence.jsonl"}}))
            graph = {"updated_at": "2026-10-31T00:00:00Z", "scorer_version": "lorem", "input_manifests": ["tasks/lorem/manifest.json"],
                     "nodes": [{"id": n, "name": n.title(), "observed_fans": 1, "avatar": {"status": "placeholder", "path": "missing.png"}} for n in ["lorem", "ipsum"]],
                     "relations": [relation("uncertain", ["ev_1"], [])]}
            (task / "graph.json").write_text(json.dumps(graph))
            output = task / "out" / "index.html"
            render(task / "graph.json", output, task)
            page = output.read_text()
            assert "<\\/script><script>alert(1)" in page and "</script><script>alert(1)" not in page


if __name__ == "__main__":
    unittest.main()
