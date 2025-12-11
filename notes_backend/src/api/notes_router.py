from typing import Optional

from fastapi import APIRouter, HTTPException, Query, status
from fastapi.responses import JSONResponse

from ..repositories.notes_repository import NotesRepository
from ..schemas.note import NoteCreate, NoteOut, NoteUpdate, NotesListOut

router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
)


@router.post(
    "",
    response_model=NoteOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a note",
    description="Create a new note with the provided title and content.",
    responses={
        201: {"description": "Note created successfully"},
        400: {"description": "Invalid input"},
    },
)
def create_note(payload: NoteCreate) -> NoteOut:
    """Create a new note."""
    repo = NotesRepository()
    note = repo.create(title=payload.title, content=payload.content)
    return NoteOut.model_validate(note)


@router.get(
    "",
    response_model=NotesListOut,
    summary="List notes",
    description="Retrieve a paginated list of notes, optionally filtered by a search query across title and content.",
)
def list_notes(
    q: Optional[str] = Query(default=None, description="Optional search query to match title or content"),
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)"),
    limit: int = Query(default=10, ge=1, le=100, description="Items per page"),
) -> NotesListOut:
    """List notes with optional search and pagination."""
    repo = NotesRepository()
    items, total = repo.list(q=q, page=page, limit=limit)
    return NotesListOut(
        total=total,
        page=page,
        limit=limit,
        items=[NoteOut.model_validate(n) for n in items],
    )


@router.get(
    "/{note_id}",
    response_model=NoteOut,
    summary="Get a note by id",
    description="Retrieve a single note by its unique identifier.",
    responses={404: {"description": "Note not found"}},
)
def get_note(note_id: int) -> NoteOut:
    """Get a specific note."""
    repo = NotesRepository()
    note = repo.get_by_id(note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return NoteOut.model_validate(note)


@router.put(
    "/{note_id}",
    response_model=NoteOut,
    summary="Update a note",
    description="Update the title and/or content of an existing note.",
    responses={404: {"description": "Note not found"}},
)
def update_note(note_id: int, payload: NoteUpdate) -> NoteOut:
    """Update an existing note."""
    repo = NotesRepository()
    note = repo.update(note_id, title=payload.title, content=payload.content)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return NoteOut.model_validate(note)


@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a note",
    description="Delete a note by its unique identifier.",
    responses={404: {"description": "Note not found"}, 204: {"description": "Note deleted"}},
)
def delete_note(note_id: int):
    """Delete a note; returns 204 on success and 404 if not found."""
    repo = NotesRepository()
    removed = repo.delete(note_id)
    if not removed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
