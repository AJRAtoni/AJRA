#!/usr/bin/env python3
"""Update AJRA.es latest posts from AJRA's public Substack.

Primary source: the publication archive API (JSON). Fallback: the RSS feed.
If both sources fail but a valid data/substack.json already exists, the
existing data is kept and the script exits successfully so a Substack
outage cannot break the Letterboxd/GameTrack update in the same workflow.
"""

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
API_URL = "https://ajra.substack.com/api/v1/archive?sort=new&limit=12"
PROFILE_URL = "https://ajra.substack.com"
CONTENT_NS = "http://purl.org/rss/1.0/modules/content/"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)
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


def fetch_url(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=45) as response:
        return response.read()


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


def posts_from_api() -> list[dict[str, object]]:
    payload = json.loads(fetch_url(API_URL))
    posts: list[dict[str, object]] = []
    for entry in payload.get("posts", []):
        title = (entry.get("title") or "").strip()
        url = (entry.get("canonical_url") or "").strip()
        image_url = (entry.get("cover_image") or "").strip()
        if not title or not url or not image_url:
            continue
        if entry.get("audience") not in (None, "everyone"):
            continue
        posts.append(
            {
                "title": title,
                "published_date": (entry.get("post_date") or "")[:10],
                "url": url,
                "image_url": image_url,
            }
        )
    posts.sort(key=lambda post: str(post["published_date"]), reverse=True)
    return posts[:4]


def posts_from_rss() -> list[dict[str, object]]:
    root = ET.fromstring(fetch_url(RSS_URL))

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
    return posts[:4]


def fetch_posts() -> list[dict[str, object]]:
    errors: list[str] = []
    for source in (posts_from_api, posts_from_rss):
        try:
            posts = source()
        except Exception as error:  # noqa: BLE001 - report and try next source
            errors.append(f"{source.__name__}: {error}")
            continue
        if len(posts) >= 4:
            return posts
        errors.append(f"{source.__name__}: only {len(posts)} usable posts")
    raise RuntimeError("Substack sources failed: " + "; ".join(errors))


def comparable(payload: dict[str, object]) -> dict[str, object]:
    return {key: value for key, value in payload.items() if key != "updated_at"}


def existing_posts() -> list[dict[str, object]]:
    try:
        current = json.loads(OUTPUT.read_text(encoding="utf-8"))
        posts = current.get("posts")
        return posts if isinstance(posts, list) else []
    except Exception:  # noqa: BLE001 - missing/corrupt file counts as no data
        return []


def main() -> int:
    try:
        posts = fetch_posts()
    except RuntimeError as error:
        if len(existing_posts()) >= 4:
            print(f"warning: {error}; keeping existing data")
            return 0
        raise

    payload: dict[str, object] = {
        "profile_url": PROFILE_URL,
        "source_url": RSS_URL,
        "posts": posts,
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

    print(f"updated {len(posts)} posts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
