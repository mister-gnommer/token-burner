import json
import tempfile
import unittest
from pathlib import Path

from evidence_pipeline import author_key, validate


SOURCE = {
    "schema_version": 1,
    "candidate_id": "src_lorem",
    "run_id": "20261030-lorem",
    "target_performer_ids": ["rafal-paczes"],
    "site": "example.com",
    "url": "https://example.com/lorem",
    "retrieved_at": "2026-10-30T00:00:00Z",
    "published_at": None,
    "author_hint": None,
    "author_key": None,
    "excerpt": "Lorem ipsum.",
    "language": "pl",
    "collector": {"provider": "example", "model": "example", "prompt_version": "example"},
}
INVALID_RECORDS = [None, [], "Lorem ipsum", {}, {"target_performer_ids": None}]


class ValidationTests(unittest.TestCase):
    def validate_records(self, records):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "records.jsonl"
            path.write_text("\n".join(json.dumps(record) for record in records), encoding="utf-8")
            return validate("source-candidate", path)

    def test_malformed_shapes_report_errors_without_crashing(self):
        count, errors = self.validate_records(INVALID_RECORDS)
        assert count == len(INVALID_RECORDS)
        assert all(any(error.startswith(f"line {line}:") for error in errors)
                   for line in range(1, count + 1))

    def test_duplicate_candidate_ids_are_rejected(self):
        assert self.validate_records([SOURCE]) == (1, [])
        assert self.validate_records([SOURCE, SOURCE]) == (
            2, ["line 2: duplicate candidate_id: src_lorem"]
        )

    def test_unknown_performers_are_rejected(self):
        record = {**SOURCE, "target_performer_ids": ["lorem-ipsum"]}
        assert self.validate_records([record]) == (
            1, ["line 1: unknown target performer IDs: ['lorem-ipsum']"]
        )

    def test_author_keys_normalize_within_a_source(self):
        assert author_key(" Example.COM ", " Lorem ") == author_key("example.com", "lorem")
        assert author_key("example.com", "lorem") != author_key("example.org", "lorem")


if __name__ == "__main__":
    unittest.main()
