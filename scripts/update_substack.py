#!/usr/bin/env python3
"""Update AJRA.es latest posts using only AJRA's public Substack RSS feed."""

from __future__ import annotations

import json
import os
import tempfile
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


RSS_URL = "https://ajra.substack.com/feed"
PROFILE_URL = "https://ajra.substack.com"
CONTENT_NS = "http://purl.org/rss/1.0/modules/content/"
ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "substack.json"


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


def image_from_html(html: str) -> str:
    parser = FirstImageParser()
    parser.feed(html)
    hostname = (urlparse(parser.src).hostname or "").lower()
    if hostname == "substackcdn.com" or hostname.endswith(".substackcdn.com"):
        return parser.src
    return ""


def fetch_posts() -> list[dict[str, object]]:
    request = urllib.request.Request(
        RSS_URL,
        headers={"User-Agent": "AJRA.es Substack sync"},
    )
    with urllib.request.urlopen(request, timeout=45) as response:
        root = ET.fromstring(response.read())

    posts: list[dict[str, object]] = []
    seen: set[str] = set()
    for item in root.findall("./channel/item"):
        title = text(item, "title")
        url = text(item, "link")
        if not title or not url or url in seen:
            continue

        enclosure = item.find("enclosure")
        image_url = (enclosure.get("url") or "").strip() if enclosure is not None else ""
        if not image_url:
            image_url = image_from_html(text(item, f"{{{CONTENT_NS}}}encoded"))
        if not image_url:
            continue

        published = ""
        pub_date = text(item, "pubDate")
        if pub_date:
            try:
                published = parsedate_to_datetime(pub_date).date().isoformat()
            except (TypeError, ValueError):
                published = ""

        seen.add(url)
        posts.append(
            {
                "title": title,
                "published_date": published,
                "url": url,
                "image_url": image_url,
            }
        )

    posts.sort(key=lambda post: str(post["published_date"]), reverse=True)
    if len(posts) < 3:
        raise RuntimeError("Substack RSS returned fewer than three usable posts")
    return posts[:3]


def comparable(payload: dict[str, object]) -> dict[str, object]:
    return {key: value for key, value in payload.items() if key != "updated_at"}


def main() -> int:
    payload: dict[str, object] = {
        "profile_url": PROFILE_URL,
        "source_url": RSS_URL,
        "posts": fetch_posts(),
    }

    if OUTPUT.exists():
        current = json.loads(OUTPUT.read_text(encoding="utf-8"))
        if comparable(current) == payload:
            print("unchanged")
            return 0

    payload["updated_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    descriptor, temporary_name = tempfile.mkstemp(dir=OUTPUT.parent, prefix="substack-", suffix=".json")
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as temporary:
            temporary.write(content)
        os.replace(temporary_name, OUTPUT)
    finally:
        if os.path.exists(temporary_name):
            os.unlink(temporary_name)

    print(f"updated {len(payload['posts'])} posts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
