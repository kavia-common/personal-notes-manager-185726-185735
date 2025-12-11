from __future__ import annotations

import sqlite3
from datetime import datetime
from typing import List, Optional, Tuple

from ..models.note import Note
from ..db.database import get_connection


class NotesRepository:
    """Repository handling SQLite operations for notes."""

    def __init__(self, connection: Optional[sqlite3.Connection] = None) -> None:
        self._own_conn = connection is None
        self.conn = connection or get_connection()

    def __del__(self) -> None:
        try:
            if self._own_conn:
                self.conn.close()
        except Exception:
            # Avoid raising in destructor
            pass

    def _row_to_note(self, row: dict) -> Note:
        return Note(
            id=row["id"],
            title=row["title"],
            content=row["content"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )

    # PUBLIC_INTERFACE
    def create(self, title: str, content: str) -> Note:
        """Create a new note and return it."""
        now = datetime.utcnow().isoformat()
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO notes (title, content, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (title, content, now, now),
        )
        note_id = cur.lastrowid
        self.conn.commit()
        return self.get_by_id(note_id)  # type: ignore

    # PUBLIC_INTERFACE
    def get_by_id(self, note_id: int) -> Optional[Note]:
        """Return a note by its id or None if not found."""
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
        row = cur.fetchone()
        if not row:
            return None
        return self._row_to_note(row)

    # PUBLIC_INTERFACE
    def list(self, q: Optional[str], page: int, limit: int) -> Tuple[List[Note], int]:
        """List notes matching optional search with pagination. Returns (items, total)."""
        conditions = []
        params: list = []
        if q:
            conditions.append("(title LIKE ? OR content LIKE ?)")
            like = f"%{q}%"
            params.extend([like, like])

        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        # Total count
        cur = self.conn.cursor()
        cur.execute(f"SELECT COUNT(*) as count FROM notes {where_clause}", params)
        total = cur.fetchone()["count"]

        # Pagination
        offset = (page - 1) * limit
        cur.execute(
            f"SELECT * FROM notes {where_clause} ORDER BY updated_at DESC, id DESC LIMIT ? OFFSET ?",
            [*params, limit, offset],
        )
        rows = cur.fetchall() or []
        items = [self._row_to_note(r) for r in rows]
        return items, int(total)

    # PUBLIC_INTERFACE
    def update(self, note_id: int, title: Optional[str], content: Optional[str]) -> Optional[Note]:
        """Update a note; returns updated note or None if not found."""
        existing = self.get_by_id(note_id)
        if not existing:
            return None
        new_title = title if title is not None else existing.title
        new_content = content if content is not None else existing.content
        now = datetime.utcnow().isoformat()
        cur = self.conn.cursor()
        cur.execute(
            "UPDATE notes SET title = ?, content = ?, updated_at = ? WHERE id = ?",
            (new_title, new_content, now, note_id),
        )
        self.conn.commit()
        return self.get_by_id(note_id)

    # PUBLIC_INTERFACE
    def delete(self, note_id: int) -> bool:
        """Delete a note by id; returns True if removed, False if not found."""
        cur = self.conn.cursor()
        cur.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        self.conn.commit()
        return cur.rowcount > 0
