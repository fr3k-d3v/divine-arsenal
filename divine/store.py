"""Local-only private profile store. No profile data belongs in the git repository."""
from __future__ import annotations
import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


def private_root() -> Path:
    root = Path(os.environ.get("DIVINE_DATA_DIR", str(Path.home() / ".local/share/divine-arsenal")))
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    root.chmod(0o700)
    return root


def _connect():
    path = private_root() / "profiles.sqlite3"
    con = sqlite3.connect(path, timeout=10)
    if path.exists():
        path.chmod(0o600)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA journal_mode=WAL")
    con.execute("""CREATE TABLE IF NOT EXISTS profiles (
        id TEXT PRIMARY KEY,
        payload TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )""")
    con.commit()
    return con


def create_profile(payload: dict) -> dict:
    item = dict(payload)
    item["id"] = str(uuid4())
    now = datetime.now(timezone.utc).isoformat()
    with _connect() as db:
        db.execute("INSERT INTO profiles(id,payload,created_at,updated_at) VALUES(?,?,?,?)",
                   (item["id"], json.dumps(item, ensure_ascii=False), now, now))
    return item


def get_profile(profile_id: str) -> dict | None:
    with _connect() as db:
        row = db.execute("SELECT payload FROM profiles WHERE id=?", (profile_id,)).fetchone()
    return json.loads(row["payload"]) if row else None


def list_profiles() -> list[dict]:
    with _connect() as db:
        rows = db.execute("SELECT id,payload FROM profiles ORDER BY updated_at DESC").fetchall()
    # List only aliases, never birth data or goals. Local browser still manages this single owner account.
    return [{"id":r["id"], "alias":json.loads(r["payload"]).get("alias", "Profile")} for r in rows]


def update_profile(profile_id: str, payload: dict) -> dict | None:
    if not get_profile(profile_id):
        return None
    item = dict(payload)
    item["id"] = profile_id
    with _connect() as db:
        db.execute("UPDATE profiles SET payload=?,updated_at=? WHERE id=?",
                   (json.dumps(item, ensure_ascii=False), datetime.now(timezone.utc).isoformat(), profile_id))
    return item


def delete_profile(profile_id: str) -> bool:
    with _connect() as db:
        cur = db.execute("DELETE FROM profiles WHERE id=?", (profile_id,))
    return cur.rowcount > 0
