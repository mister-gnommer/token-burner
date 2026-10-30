#!/usr/bin/env python3
import argparse
import hashlib
import json
import sys
from pathlib import Path

import jsonschema

TASK_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = TASK_ROOT / "data" / "schemas"
SCHEMAS = {
    "source-candidate": "source-candidate.schema.json",
    "evidence": "evidence-v2.schema.json",
    "evidence-v1": "evidence.schema.json",
    "relation": "relation-candidate.schema.json",
    "run-manifest": "run-manifest.schema.json",
}
ID_FIELDS = {
    "source-candidate": "candidate_id",
    "evidence": "id",
    "evidence-v1": "id",
    "relation": "id",
    "run-manifest": "run_id",
}


def load_records(path):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".jsonl":
        records = []
        for line_number, line in enumerate(text.splitlines(), start=1):
            if line.strip():
                try:
                    records.append((f"line {line_number}", json.loads(line)))
                except json.JSONDecodeError as error:
                    raise ValueError(f"{path}:{line_number}: {error.msg}") from error
        return records
    data = json.loads(text)
    if isinstance(data, list):
        return [(f"item {index}", record) for index, record in enumerate(data, start=1)]
    return [("document", data)]


def valid_performer_ids():
    ranking = json.loads(
        (TASK_ROOT / "data" / "standupers.json").read_text(encoding="utf-8")
    )
    return {performer["id"] for performer in ranking["performers"]}


def semantic_errors(kind, location, record, performer_ids):
    errors = []
    if kind == "source-candidate":
        unknown = set(record["target_performer_ids"]) - performer_ids
        if unknown:
            errors.append(f"unknown target performer IDs: {sorted(unknown)}")
    elif kind in {"evidence", "evidence-v1"}:
        unknown = {
            mention["performer_id"]
            for mention in record["mentions"]
            if mention["performer_id"] is not None
        } - performer_ids
        if unknown:
            errors.append(f"unknown mentioned performer IDs: {sorted(unknown)}")
        if (
            record["review"]["status"] == "accepted"
            and not record["review"]["reviewer"]
        ):
            errors.append("accepted evidence has no reviewer")
    elif kind == "relation":
        pair = record["pair"]
        if pair != sorted(pair):
            errors.append("relation pair is not lexicographically sorted")
        unknown = set(pair) - performer_ids
        if unknown:
            errors.append(f"unknown relation performer IDs: {sorted(unknown)}")
    elif kind == "run-manifest":
        unknown = set(record["performer_ids"]) - performer_ids
        if unknown:
            errors.append(f"unknown manifest performer IDs: {sorted(unknown)}")
    return [f"{location}: {error}" for error in errors]


def validate(kind, path):
    schema = json.loads((SCHEMA_DIR / SCHEMAS[kind]).read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(
        schema, format_checker=jsonschema.FormatChecker()
    )
    performer_ids = valid_performer_ids()
    records = load_records(path)
    errors = []
    seen_ids = set()
    id_field = ID_FIELDS[kind]
    for location, record in records:
        schema_errors = sorted(
            validator.iter_errors(record), key=lambda item: list(item.path)
        )
        for error in schema_errors:
            pointer = "/".join(str(part) for part in error.path)
            suffix = f" at {pointer}" if pointer else ""
            errors.append(f"{location}: {error.message}{suffix}")
        if schema_errors:
            continue
        errors.extend(semantic_errors(kind, location, record, performer_ids))
        record_id = record.get(id_field)
        if record_id is not None:
            if record_id in seen_ids:
                errors.append(f"{location}: duplicate {id_field}: {record_id}")
            seen_ids.add(record_id)
    return len(records), errors


def author_key(site, author):
    normalized = f"{site.strip().lower()}:{author.strip().casefold()}"
    digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    return f"fan_{digest[:16]}"


def main():
    parser = argparse.ArgumentParser(
        description="Validate standupers graph data and derive pseudonymous fan keys"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("--kind", choices=sorted(SCHEMAS), required=True)
    validate_parser.add_argument("path", type=Path)
    key_parser = subparsers.add_parser("author-key")
    key_parser.add_argument("--site", required=True)
    key_parser.add_argument("--author", required=True)
    args = parser.parse_args()
    if args.command == "author-key":
        print(author_key(args.site, args.author))
        return 0
    try:
        count, errors = validate(args.kind, args.path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(str(error), file=sys.stderr)
        return 1
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"validated {count} {args.kind} record(s): {args.path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
