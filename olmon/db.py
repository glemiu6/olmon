import datetime
import sqlite3
from pathlib import Path

from platformdirs import user_data_dir

DB_PATH = Path(user_data_dir("olmon")) / "models.db"

VRAM_OVERHEAD_FACTOR = 1.2


def estimate_vram_bytes(size_bytes: int) -> int:
    """Rough estimate of actual VRAM needed to run a model, given its file size."""
    return int(size_bytes * VRAM_OVERHEAD_FACTOR)


SCHEMA = """

CREATE TABLE IF NOT EXISTS models (
    name TEXT PRIMARY KEY,
    description TEXT,
    capabilities TEXT,
    pulls INTEGER,
    tag_count INTEGER,
    updated_text TEXT,
    scraped_at TEXT
);

CREATE TABLE IF NOT EXISTS model_tags (
    full_name TEXT PRIMARY KEY,
    model_name TEXT NOT NULL REFERENCES models(name),
    tag TEXT,
    size_bytes INTEGER,
    context_length INTEGER,
    input_type TEXT,
    digest TEXT,
    is_default INTEGER DEFAULT 0,
    updated_text TEXT,
    scraped_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_model_tags_model_name ON model_tags(model_name);
CREATE INDEX IF NOT EXISTS idx_model_tags_size ON model_tags(size_bytes);
"""


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)
    return conn


def now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def upsert_model(conn: sqlite3.Connection, model: dict) -> None:
    conn.execute(
        """
        INSERT INTO models (name, description, capabilities, pulls, tag_count, updated_text, scraped_at)
        VALUES (:name, :description, :capabilities, :pulls, :tag_count, :updated_text, :scraped_at)
        ON CONFLICT(name) DO UPDATE SET
            description = excluded.description,
            capabilities = excluded.capabilities,
            pulls = excluded.pulls,
            tag_count = excluded.tag_count,
            updated_text = excluded.updated_text,
            scraped_at = excluded.scraped_at
        """,  # noqa: E501
        model,  # noqa: E501
    )


def upsert_tag(conn: sqlite3.Connection, tag: dict) -> None:
    conn.execute(
        """
        INSERT INTO model_tags (full_name, model_name, tag, size_bytes, context_length, input_type, digest, is_default, updated_text, scraped_at)
        VALUES (:full_name, :model_name, :tag, :size_bytes, :context_length, :input_type, :digest, :is_default, :updated_text, :scraped_at)
        ON CONFLICT(full_name) DO UPDATE SET
            size_bytes = excluded.size_bytes,
            context_length = excluded.context_length,
            input_type = excluded.input_type,
            digest = excluded.digest,
            is_default = excluded.is_default,
            updated_text = excluded.updated_text,
            scraped_at = excluded.scraped_at
        """,  # noqa: E501
        tag,
    )


def get_stat(conn: sqlite3.Connection) -> dict:
    model_count = conn.execute("SELECT COUNT(*) FROM models").fetchone()[0]
    tag_count = conn.execute("SELECT COUNT(*) FROM model_tags").fetchone()[0]
    last_scrape = conn.execute("SELECT MAX(scraped_at) FROM models").fetchone()[0]
    db_size = DB_PATH.stat().st_size if DB_PATH.exists() else 0
    return {
        "model_count": model_count,
        "tag_count": tag_count,
        "last_scrape": last_scrape,
        "db_size": db_size,
        "db_path": str(DB_PATH),
    }  # noqa: E501


def search_models(conn: sqlite3.Connection, query: str, limit: int = 20) -> list[sqlite3.Row]:
    conn.row_factory = sqlite3.Row
    like = f"%{query.lower()}%"
    return conn.execute(
        """
        SELECT * FROM models
        WHERE lower(name) LIKE ? or lower(description) LIKE ?
        ORDER BY pulls DESC
        LIMIT ?
        """,
        (like, like, limit),
    ).fetchall()


def get_tags_for_model(conn: sqlite3.Connection, model_name: str) -> list[sqlite3.Row]:
    conn.row_factory = sqlite3.Row
    return conn.execute(
        "SELECT * FROM model_tags WHERE model_name = ? ORDER BY size_bytes DESC", (model_name,)
    ).fetchall()


def find_tags_under_size(
    conn: sqlite3.Connection, max_bytes: int, limit: int = 20
) -> list[sqlite3.Row]:
    conn.row_factory = sqlite3.Row
    file_size_threashold = int(max_bytes / VRAM_OVERHEAD_FACTOR)
    return conn.execute(
        """
        WITH ranked AS (
            SELECT model_tags.*, models.description, models.pulls,
                   ROW_NUMBER() OVER (
                       PARTITION BY model_tags.model_name
                       ORDER BY model_tags.size_bytes DESC
                   ) AS rn
            FROM model_tags
            JOIN models ON models.name = model_tags.model_name
            WHERE size_bytes IS NOT NULL AND size_bytes <= ?
        )
        SELECT * FROM ranked
        WHERE rn = 1
        ORDER BY pulls DESC
        LIMIT ?

        """,
        (file_size_threashold, limit),
    ).fetchall()
