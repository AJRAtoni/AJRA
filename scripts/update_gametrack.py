#!/usr/bin/env python3
"""Update AJRA.es with AJRA's pinned in-progress games."""

from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


USERNAME = "ajra"
PROFILE_URL = f"https://gametrack.app/user/{USERNAME}/playing"
ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "gametrack.json"
PINNED_GAMES: list[dict[str, Any]] = [
    {
        "id": 338079,
        "title": "Elden Ring: Tarnished Edition",
        "platform": "Switch 2",
        "url": "https://gametrack.app/game/338079",
        "poster_url": "https://images.igdb.com/igdb/image/upload/t_cover_big_2x/coc8ea.jpg",
    },
    {
        "id": 1877,
        "title": "Cyberpunk 2077",
        "platform": "Switch 2",
        "url": "https://gametrack.app/game/1877",
        "poster_url": "https://images.igdb.com/igdb/image/upload/t_cover_big_2x/coaih8.jpg",
    },
    {
        "id": 337036,
        "title": "Tomodachi Life: Living the Dream",
        "platform": "Switch 2",
        "url": "https://gametrack.app/game/337036",
        "poster_url": "https://images.igdb.com/igdb/image/upload/t_cover_big_2x/cobdqd.jpg",
    },
]


def fetch_games() -> list[dict[str, Any]]:
    return [game.copy() for game in PINNED_GAMES]


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
