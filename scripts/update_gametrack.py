#!/usr/bin/env python3
"""Update AJRA.es in-progress games from AJRA's public GameTrack profile."""

from __future__ import annotations

import json
import os
import tempfile
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


USERNAME = "ajra"
PROFILE_URL = f"https://gametrack.app/user/{USERNAME}/playing"
PROJECT_ID = "firebase-gametrack"
API_KEY = "AIzaSyC7C-64IEIr30EGILwbOiaOZJttEpfpsUw"
FIRESTORE_ROOT = (
    f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}"
    "/databases/(default)/documents"
)
ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "gametrack.json"


def request_json(url: str, body: dict[str, Any] | None = None) -> Any:
    data = json.dumps(body).encode("utf-8") if body is not None else None
    request = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "AJRA.es GameTrack sync",
        },
        method="POST" if body is not None else "GET",
    )
    with urllib.request.urlopen(request, timeout=45) as response:
        return json.load(response)


def user_id() -> str:
    query = {
        "structuredQuery": {
            "select": {"fields": [{"fieldPath": "username"}]},
            "from": [{"collectionId": "users"}],
            "where": {
                "fieldFilter": {
                    "field": {"fieldPath": "username"},
                    "op": "EQUAL",
                    "value": {"stringValue": USERNAME},
                }
            },
            "limit": 1,
        }
    }
    endpoint = f"{FIRESTORE_ROOT}:runQuery?{urllib.parse.urlencode({'key': API_KEY})}"
    results = request_json(endpoint, query)
    document = next((item.get("document") for item in results if item.get("document")), None)
    if not document:
        raise RuntimeError(f"GameTrack profile @{USERNAME} was not found")
    return str(document["name"]).rsplit("/", 1)[-1]


def scalar(fields: dict[str, Any], name: str, default: Any = "") -> Any:
    value = fields.get(name, {})
    for kind in ("stringValue", "integerValue", "doubleValue", "booleanValue"):
        if kind in value:
            return value[kind]
    return default


def cover_url(source: str) -> str:
    if not source.startswith("https://images.igdb.com/igdb/image/upload/"):
        return ""
    filename = Path(urllib.parse.urlparse(source).path).stem
    if not filename:
        return ""
    return f"https://images.igdb.com/igdb/image/upload/t_cover_big_2x/{filename}.jpg"


def fetch_games() -> list[dict[str, Any]]:
    uid = user_id()
    query = urllib.parse.urlencode(
        {
            "key": API_KEY,
            "pageSize": 100,
            "orderBy": "date desc",
        }
    )
    endpoint = f"{FIRESTORE_ROOT}/posts/{uid}/nowPlaying?{query}"
    response = request_json(endpoint)

    games: list[dict[str, Any]] = []
    seen: set[int] = set()
    for document in response.get("documents", []):
        game = (
            document.get("fields", {})
            .get("game", {})
            .get("mapValue", {})
            .get("fields", {})
        )
        game_id = int(scalar(game, "gameID", 0))
        title = str(scalar(game, "title", "")).strip()
        poster = cover_url(str(scalar(game, "posterURL", "")))
        if not game_id or not title or not poster or game_id in seen:
            continue

        seen.add(game_id)
        games.append(
            {
                "id": game_id,
                "title": title,
                "platform": str(scalar(game, "ownedPlatform", "")),
                "url": f"https://gametrack.app/game/{game_id}",
                "poster_url": poster,
            }
        )
        if len(games) == 3:
            break

    if len(games) < 3:
        raise RuntimeError("GameTrack returned fewer than three usable games")
    return games


def comparable(payload: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in payload.items() if key != "updated_at"}


def main() -> int:
    payload: dict[str, Any] = {
        "profile_url": PROFILE_URL,
        "source_url": PROFILE_URL,
        "games": fetch_games(),
    }

    if OUTPUT.exists():
        current = json.loads(OUTPUT.read_text(encoding="utf-8"))
        if comparable(current) == payload:
            print("unchanged")
            return 0

    payload["updated_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    descriptor, temporary_name = tempfile.mkstemp(dir=OUTPUT.parent, prefix="gametrack-", suffix=".json")
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as temporary:
            temporary.write(content)
        os.replace(temporary_name, OUTPUT)
    finally:
        if os.path.exists(temporary_name):
            os.unlink(temporary_name)

    print(f"updated {len(payload['games'])} games")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
