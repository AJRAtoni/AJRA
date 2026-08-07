#!/usr/bin/env python3
"""Update AJRA.es recent films using only AJRA's public Letterboxd RSS feed."""

from __future__ import annotations

import json
import os
import tempfile
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


RSS_URL = "https://letterboxd.com/ajra/rss/"
PROFILE_URL = "https://letterboxd.com/ajra/"
LETTERBOXD_NS = "https://letterboxd.com"
ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "letterboxd.json"


class FirstImageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.src = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "img" or self.src:
            return
        values = dict(attrs)
        self.src = values.get("src") or ""


def text(item: ET.Element, name: str) -> str:
    value = item.findtext(name)
    return value.strip() if value else ""


def rating_text(value: str) -> str:
    if not value:
        return ""
    rating = float(value)
    full = int(rating)
    return "★" * full + ("½" if rating - full >= 0.5 else "")


def poster_from(description: str) -> str:
    parser = FirstImageParser()
    parser.feed(description)
    hostname = (urlparse(parser.src).hostname or "").lower()
    if hostname == "ltrbxd.com" or hostname.endswith(".ltrbxd.com"):
        return parser.src
    return ""


def fetch_films() -> list[dict[str, object]]:
    request = urllib.request.Request(
        RSS_URL,
        headers={"User-Agent": "AJRA.es Letterboxd sync"},
    )
    with urllib.request.urlopen(request, timeout=45) as response:
        root = ET.fromstring(response.read())

    films: list[dict[str, object]] = []
    seen: set[str] = set()
    for item in root.findall("./channel/item"):
        title = text(item, f"{{{LETTERBOXD_NS}}}filmTitle")
        watched_date = text(item, f"{{{LETTERBOXD_NS}}}watchedDate")
        url = text(item, "link")
        if not title or not watched_date or not url or url in seen:
            continue

        description = text(item, "description")
        poster_url = poster_from(description)
        if not poster_url:
            continue

        rating = text(item, f"{{{LETTERBOXD_NS}}}memberRating")
        seen.add(url)
        films.append(
            {
                "title": title,
                "year": text(item, f"{{{LETTERBOXD_NS}}}filmYear"),
                "watched_date": watched_date,
                "rating": float(rating) if rating else None,
                "rating_text": rating_text(rating),
                "rewatch": text(item, f"{{{LETTERBOXD_NS}}}rewatch").lower() == "yes",
                "url": url,
                "poster_url": poster_url,
            }
        )

    films.sort(key=lambda film: str(film["watched_date"]), reverse=True)
    if len(films) < 3:
        raise RuntimeError("Letterboxd RSS returned fewer than three usable diary entries")
    return films[:3]


def comparable(payload: dict[str, object]) -> dict[str, object]:
    return {key: value for key, value in payload.items() if key != "updated_at"}


def main() -> int:
    payload: dict[str, object] = {
        "profile_url": PROFILE_URL,
        "source_url": RSS_URL,
        "films": fetch_films(),
    }

    if OUTPUT.exists():
        current = json.loads(OUTPUT.read_text(encoding="utf-8"))
        if comparable(current) == payload:
            print("unchanged")
            return 0

    payload["updated_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    descriptor, temporary_name = tempfile.mkstemp(dir=OUTPUT.parent, prefix="letterboxd-", suffix=".json")
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as temporary:
            temporary.write(content)
        os.replace(temporary_name, OUTPUT)
    finally:
        if os.path.exists(temporary_name):
            os.unlink(temporary_name)

    print(f"updated {len(payload['films'])} films")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
