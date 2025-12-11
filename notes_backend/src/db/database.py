import sqlite3
from pathlib import Path

from ..core.config import get_settings

# SQLite row factory to return dict-like rows
def dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


def _ensure_data_dir(db_path: str) -> None:
    """Ensure the parent directory for the SQLite DB exists."""
    parent = Path(db_path).expanduser().resolve().parent
    parent.mkdir(parents=True, exist_ok=True)


def _initialize_schema(conn: sqlite3.Connection) -> None:
    """Create tables if not existing."""
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        """
    )
    conn.commit()


# PUBLIC_INTERFACE
def get_connection() -> sqlite3.Connection:
    """Returns a sqlite3 connection configured with row factory."""
    settings = get_settings()
    db_path = settings.notes_db_path
    _ensure_data_dir(db_path)
    conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES, check_same_thread=False)
    conn.row_factory = dict_factory
    return conn


# PUBLIC_INTERFACE
def initialize_database() -> None:
    """Ensure database file and schema exist."""
    conn = get_connection()
    try:
        _initialize_schema(conn)
    finally:
        conn.close()
