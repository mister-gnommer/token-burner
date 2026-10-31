import copy
import json
import tempfile
import unittest
from pathlib import Path

from graph_pipeline import TASK_ROOT, aggregate, d2_source, load_evidence

FIXTURE_ROOT = TASK_ROOT / "fixtures/synthetic-graph"
PERFORMERS = json.loads((FIXTURE_ROOT / "ranking.json").read_text())["performers"]
RECORDS = [json.loads(line) for line in (FIXTURE_ROOT / "evidence.jsonl").read_text().splitlines()]
UPDATED_AT = "2026-10-30T00:00:00Z"


def rejects_load(paths, root, synthetic):
    try:
        load_evidence(paths, root, synthetic)
    except ValueError:
        return True
    return False


class GraphTests(unittest.TestCase):
    def test_normalizes_coverage_and_deduplicates_fans(self):
        relations, deferred, coverage = aggregate(PERFORMERS, RECORDS, UPDATED_AT)
        actual = {tuple(r["pair"]): (r["status"], r["independent_fan_count"], r["score"]) for r in relations}
        assert actual == {
            ("ipsum", "lorem"): ("accepted", 2, 0.5),
            ("dolor", "ipsum"): ("accepted", 2, 0.5),
            ("amet", "lorem"): ("uncertain", 0, 0.0),
        }
        assert coverage == {"amet": 1, "dolor": 2, "ipsum": 4, "isolated": 0, "lorem": 2}
        assert deferred == []

    def test_repeated_names_do_not_create_self_edges_or_extra_support(self):
        record = copy.deepcopy(RECORDS[0])
        record["mentions"].append(copy.deepcopy(record["mentions"][0]))
        relations, _, _ = aggregate(PERFORMERS, [record], UPDATED_AT)
        assert [(r["pair"], r["independent_fan_count"], r["status"]) for r in relations] == [(["ipsum", "lorem"], 1, "uncertain")]

    def test_opposing_preferences_prevent_an_accepted_edge(self):
        opposing = copy.deepcopy(RECORDS[0])
        opposing["id"] = "ev_synthetic_opposed"
        opposing["mentions"][0]["sentiment"] = "negative"
        opposing["evidence_class"] = "fan_comparison"
        relations, _, _ = aggregate(PERFORMERS, RECORDS[:2] + [opposing], UPDATED_AT)
        assert relations[0]["status"] == "uncertain"
        assert relations[0]["contradictory_evidence_ids"] == ["ev_synthetic_opposed"]

    def test_neutral_mentions_and_comparisons_never_create_support(self):
        for sentiment, evidence_class in [("neutral", "same_user_coendorsement"), ("positive", "fan_comparison")]:
            records = copy.deepcopy(RECORDS[:2])
            for record in records:
                record["mentions"][0]["sentiment"] = sentiment
                record["evidence_class"] = evidence_class
            assert aggregate(PERFORMERS, records, UPDATED_AT)[0] == []

    def test_uncertain_mixed_unresolved_and_low_confidence_records_are_deferred(self):
        for field, value in [("review", "uncertain"), ("sentiment", "mixed"), ("performer_id", None), ("confidence", 0.4)]:
            record = copy.deepcopy(RECORDS[0])
            if field == "review":
                record["review"]["status"] = value
            else:
                record["mentions"][0][field] = value
            relations, deferred, _ = aggregate(PERFORMERS, [record], UPDATED_AT)
            assert relations == []
            assert len(deferred) == 1

    def test_calibration_never_enters_the_graph(self):
        path = TASK_ROOT / "reports/runs/20261030-stage03-context-calibration.json"
        records, ignored = load_evidence([path], TASK_ROOT, False)
        assert records == []
        assert len(ignored) == 1

    def test_source_lineage_and_synthetic_separation(self):
        records, ignored = load_evidence([FIXTURE_ROOT / "manifest.json"], FIXTURE_ROOT, True)
        assert records == RECORDS and ignored == []
        assert rejects_load([FIXTURE_ROOT / "manifest.json"], FIXTURE_ROOT, False)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for path in FIXTURE_ROOT.iterdir():
                (root / path.name).write_bytes(path.read_bytes())
            bad = copy.deepcopy(RECORDS)
            bad[0]["excerpt"] = "Lorem ipsum changed."
            (root / "evidence.jsonl").write_text("\n".join(json.dumps(r) for r in bad))
            assert rejects_load([root / "manifest.json"], root, True)

    def test_renderer_keeps_isolates_and_hides_opposing_only_edges(self):
        relations, _, coverage = aggregate(PERFORMERS, RECORDS, UPDATED_AT)
        graph = {"synthetic": True, "nodes": [{**p, "observed_fans": coverage[p["id"]]} for p in PERFORMERS], "relations": relations, "evidence_sources": {r["id"]: r["source"]["url"] for r in RECORDS}}
        source = d2_source(graph)
        assert source.count(" -- ") == 2
        assert "Isolated" in source and "SYNTHETIC" in source
        assert "Layout distance has no similarity meaning" in source
        assert "tooltip:" in source

    def test_batch_view_retains_selected_isolates_without_implicit_hidden_nodes(self):
        relations, _, coverage = aggregate(PERFORMERS, RECORDS, UPDATED_AT)
        graph = {"synthetic": True, "nodes": [{**p, "observed_fans": coverage[p["id"]]} for p in PERFORMERS], "relations": relations, "evidence_sources": {r["id"]: r["source"]["url"] for r in RECORDS}, "visible_node_ids": ["isolated", "ipsum", "lorem"]}
        source = d2_source(graph)
        assert "Isolated" in source and "Dolor" not in source and "Amet" not in source
        assert source.count(" -- ") == 1
        assert len(graph["nodes"]) == 5

    def test_v3_localizes_ambiguous_mentions_and_keeps_qualified_liking(self):
        record = copy.deepcopy(RECORDS[0])
        record.update(schema_version=3, context=[])
        for mention in record["mentions"]:
            mention.update(preference="positive", preference_quote=record["excerpt"])
        record["mentions"][0]["sentiment"] = "mixed"
        unknown = copy.deepcopy(record["mentions"][0])
        unknown.update(performer_id=None, confidence=0.3, preference="unknown", preference_quote=None)
        record["mentions"].append(unknown)
        relations, deferred, coverage = aggregate(PERFORMERS, [record], UPDATED_AT)
        assert relations[0]["independent_fan_count"] == 1
        assert len(deferred) == 1 and deferred[0]["performer_id"] is None
        assert coverage["ipsum"] == coverage["lorem"] == 1
        record["mentions"][0]["preference"] = "unknown"
        record["mentions"][0]["preference_quote"] = None
        assert aggregate(PERFORMERS, [record], UPDATED_AT)[0] == []

    def test_one_fan_is_dashed_but_opposed_pair_is_hidden(self):
        relations, _, coverage = aggregate(PERFORMERS, RECORDS[:1], UPDATED_AT)
        graph = {"synthetic": True, "nodes": [{**p, "observed_fans": coverage[p["id"]]} for p in PERFORMERS], "relations": relations, "evidence_sources": {r["id"]: r["source"]["url"] for r in RECORDS}}
        source = d2_source(graph)
        assert source.count(" -- ") == 1 and "style.stroke-dash: 5" in source and "PROVISIONAL" in source
        relations[0]["contradictory_evidence_ids"] = ["ev_synthetic_opposed"]
        assert " -- " not in d2_source(graph)

    def test_v3_loader_rejects_invented_quotes_and_changed_context(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for path in FIXTURE_ROOT.iterdir():
                (root / path.name).write_bytes(path.read_bytes())
            candidates = [json.loads(line) for line in (root / "source-candidates.jsonl").read_text().splitlines()]
            records = copy.deepcopy(RECORDS)
            for candidate, record in zip(candidates, records):
                excerpt = "Lorem ipsum " + candidate["candidate_id"] + ": " + " ".join(m["surface_form"] for m in record["mentions"])
                candidate.update(schema_version=2, context=[], excerpt=excerpt)
                record.update(schema_version=3, context=[], excerpt=excerpt)
                for mention in record["mentions"]:
                    mention.update(preference=mention["sentiment"], preference_quote=excerpt)
            (root / "source-candidates.jsonl").write_text("\n".join(json.dumps(r) for r in candidates))
            (root / "evidence.jsonl").write_text("\n".join(json.dumps(r) for r in records))
            assert len(load_evidence([root / "manifest.json"], root, True)[0]) == len(records)
            for alteration in ["quote", "context"]:
                bad = copy.deepcopy(records)
                if alteration == "quote":
                    bad[0]["mentions"][0]["preference_quote"] = "Invented lorem quotation."
                else:
                    bad[0]["context"] = [{"role": "parent", "url": "https://example.invalid/parent", "author_hint": None, "author_key": None, "excerpt": "Lorem ipsum?"}]
                (root / "evidence.jsonl").write_text("\n".join(json.dumps(r) for r in bad))
                assert rejects_load([root / "manifest.json"], root, True)


if __name__ == "__main__":
    unittest.main()
