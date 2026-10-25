#!/usr/bin/env python3
import argparse
import hashlib
import json
import time
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen

BASE_URL = "https://standup.pl/komicy"
PAGE_SIZE = 9
USER_AGENT = (
    "StandupersGraphResearch/0.1 (+https://github.com/mister-gnommer/token-burner)"
)
TASK_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = TASK_ROOT / "data"


class JsonLdParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_json_ld = False
        self.chunks = []
        self.documents = []

    def handle_starttag(self, tag, attrs):
        if tag == "script" and dict(attrs).get("type") == "application/ld+json":
            self.in_json_ld = True
            self.chunks = []

    def handle_data(self, data):
        if self.in_json_ld:
            self.chunks.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self.in_json_ld:
            self.documents.append("".join(self.chunks))
            self.in_json_ld = False


def now_iso():
    return (
        datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    )


def date_stamp():
    return datetime.now(timezone.utc).strftime("%Y%m%d")


def fetch_catalog_page(page):
    url = f"{BASE_URL}?sort=views&page={page}"
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=30) as response:
        html = response.read().decode("utf-8", "replace")
    parser = JsonLdParser()
    parser.feed(html)
    for document in parser.documents:
        data = json.loads(document)
        if (
            data.get("@type") == "ItemList"
            and data.get("name") == "Polscy komicy stand-up"
        ):
            return url, html, data
    raise ValueError(f"Catalog ItemList not found on page {page}")


def fetch_candidates(pages):
    candidates = []
    fetched_pages = []
    retrieved_at = now_iso()
    for page in range(1, pages + 1):
        if page > 1:
            time.sleep(0.25)
        url, html, data = fetch_catalog_page(page)
        items = data["itemListElement"]
        if not items:
            raise ValueError(f"Page {page} is empty; adjust the requested page count")
        fetched_pages.append(
            {
                "page": page,
                "url": url,
                "sha256": hashlib.sha256(html.encode("utf-8")).hexdigest(),
                "item_count": len(items),
            }
        )
        for item in items:
            candidates.append(
                {
                    "source_position": item["position"],
                    "source_page": page,
                    "name": item["name"],
                    "profile_url": item["url"],
                    "image_url": item.get("image"),
                }
            )
    positions = [candidate["source_position"] for candidate in candidates]
    if positions != list(range(1, pages * PAGE_SIZE + 1)):
        raise ValueError(
            "Catalog positions are not contiguous; refusing to freeze a partial order"
        )
    profile_urls = [candidate["profile_url"] for candidate in candidates]
    if len(profile_urls) != len(set(profile_urls)):
        raise ValueError("Duplicate performer profile URLs in catalog candidates")
    return {
        "schema_version": 1,
        "source": {
            "site": "standup.pl",
            "sort": "views",
            "retrieved_at": retrieved_at,
            "page_size": PAGE_SIZE,
            "pages": fetched_pages,
        },
        "candidates": candidates,
    }


def finalize(date):
    candidates_path = DATA_DIR / f"ranking-candidates-{date}.json"
    decisions_path = DATA_DIR / f"ranking-decisions-{date}.json"
    candidates_document = json.loads(candidates_path.read_text(encoding="utf-8"))
    decisions_document = json.loads(decisions_path.read_text(encoding="utf-8"))
    candidates = candidates_document["candidates"]
    decisions = decisions_document["decisions"]
    by_position = {candidate["source_position"]: candidate for candidate in candidates}
    if {item["source_position"] for item in decisions} != set(by_position):
        raise ValueError(
            "Every candidate must have exactly one include/exclude decision"
        )
    if len(decisions) != len(candidates):
        raise ValueError("Duplicate decisions detected")
    eligible = []
    for decision in sorted(decisions, key=lambda item: item["source_position"]):
        candidate = by_position[decision["source_position"]]
        if decision["name"] != candidate["name"]:
            raise ValueError(
                f"Decision name does not match candidate at source position {decision['source_position']}"
            )
        if decision["decision"] not in {"include", "exclude"}:
            raise ValueError(
                f"Unresolved decision at source position {decision['source_position']}"
            )
        if decision["decision"] == "include":
            eligible.append(decision)
    if len(eligible) < 100:
        raise ValueError(
            f"Only {len(eligible)} included candidates; fetch more pages before freezing"
        )
    selected = eligible[:100]
    performers = []
    for rank, decision in enumerate(selected, start=1):
        candidate = by_position[decision["source_position"]]
        performer_id = candidate["profile_url"].rstrip("/").rsplit("/", 1)[-1]
        performers.append(
            {
                "rank": rank,
                "id": performer_id,
                "name": candidate["name"],
                "profile_url": candidate["profile_url"],
                "image_url": candidate["image_url"],
                "source_position": candidate["source_position"],
                "aliases": [],
                "batch": (rank - 1) // 10 + 1,
                "status": "pending",
            }
        )
    ids = [performer["id"] for performer in performers]
    if len(ids) != len(set(ids)):
        raise ValueError("Performer IDs derived from profile URLs are not unique")
    output = {
        "schema_version": 1,
        "frozen_at": now_iso(),
        "source": candidates_document["source"],
        "selection": {
            "rule": "First 100 entries marked include in source order; groups, channels, and formats are excluded before ranking",
            "decisions_file": decisions_path.name,
            "candidate_count": len(candidates),
            "eligible_candidate_count": len(eligible),
            "selected_count": len(selected),
        },
        "performers": performers,
    }
    output_path = DATA_DIR / "standupers.json"
    output_path.write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"Froze {len(performers)} performers from {len(candidates)} reviewed candidates: {output_path}"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Fetch and freeze the standup.pl performer ranking"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    fetch_parser = subparsers.add_parser("fetch")
    fetch_parser.add_argument("--pages", type=int, default=15)
    fetch_parser.add_argument("--date", default=date_stamp())
    finalize_parser = subparsers.add_parser("finalize")
    finalize_parser.add_argument("--date", default=date_stamp())
    args = parser.parse_args()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if args.command == "fetch":
        if args.pages < 12:
            raise ValueError(
                "Fetch at least 12 pages so there are enough candidates for 100 performers"
            )
        document = fetch_candidates(args.pages)
        output_path = DATA_DIR / f"ranking-candidates-{args.date}.json"
        output_path.write_text(
            json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"Saved {len(document['candidates'])} candidates: {output_path}")
    else:
        finalize(args.date)


if __name__ == "__main__":
    main()
