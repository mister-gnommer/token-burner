import json
import re
import tempfile
import unittest
from pathlib import Path

from render_interactive import TEMPLATE, edge_kind, explanation_counts, render


def relation(status, support, opposing):
    return {"pair": ["lorem", "ipsum"], "status": status, "support_evidence_ids": support, "contradictory_evidence_ids": opposing,
            "score": 0.5, "confidence": 0.9, "independent_fan_count": len(support), "explanation": "Lorem."}


class InteractiveRenderTests(unittest.TestCase):
    def test_opposing_evidence_never_attracts_even_when_accepted(self):
        assert edge_kind(relation("accepted", ["ev_1", "ev_2"], [])) == "accepted"
        assert edge_kind(relation("uncertain", ["ev_1"], [])) == "provisional"
        assert edge_kind(relation("accepted", ["ev_1", "ev_2"], ["ev_3"])) == "contested"
        assert edge_kind(relation("uncertain", [], ["ev_3"])) == "contested"

    def test_explanation_counts_parse_scorer_sentences_only(self):
        accepted = ("2 source-scoped fans explicitly co-endorse this pair; 24 observed fans endorse either performer. "
                    "0 opposing preference records. Provisional observed overlap.")
        assert explanation_counts(accepted) == {"fans": 2, "observed": 24, "opposing": 0, "accepted": True}
        uncertain = ("1 source-scoped fans explicitly co-endorse this pair; 9 observed fans endorse either performer. "
                     "3 opposing preference records. Insufficient independent support or opposing preferences; "
                     "eligible uncontested one-fan pairs may be shown as provisional.")
        assert explanation_counts(uncertain) == {"fans": 1, "observed": 9, "opposing": 3, "accepted": False}
        assert explanation_counts("Lorem.") is None

    def test_every_ui_language_defines_the_same_strings(self):
        template = TEMPLATE.read_text()
        blocks = re.search(r"const I18N = \{\n  en: \{(.*?)\n  \},\n  pl: \{(.*?)\n  \},\n\};", template, re.S)
        keys = [set(re.findall(r"^\s{4}(\w+):|, (\w+):", block, re.M)) for block in blocks.groups()]
        en, pl = ({k for pair in found for k in pair if k} for found in keys)
        assert en == pl, en ^ pl
        used = set(re.findall(r'\bt\("(\w+)"', template)) | set(re.findall(r'data-i18n(?:-attr)?="([^"]+)"', template))
        used = {part.split(":")[-1] for item in used for part in item.split(";")}
        assert used <= en, used - en

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
