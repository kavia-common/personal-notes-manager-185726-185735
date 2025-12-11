from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    title: str = Field(..., description="Title of the note", min_length=1, max_length=255)
    content: str = Field(..., description="Content/body of the note")


class NoteCreate(NoteBase):
    """Schema for note creation payload."""
    pass


class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Updated title of the note", min_length=1, max_length=255)
    content: Optional[str] = Field(None, description="Updated content/body of the note")


class NoteOut(NoteBase):
    id: int = Field(..., description="Unique identifier for the note")
    created_at: datetime = Field(..., description="Timestamp when the note was created")
    updated_at: datetime = Field(..., description="Timestamp when the note was last updated")

    class Config:
        from_attributes = True


class NotesListOut(BaseModel):
    total: int = Field(..., description="Total number of notes matching the query")
    page: int = Field(..., description="Current page number (1-indexed)")
    limit: int = Field(..., description="Number of items per page")
    items: List[NoteOut] = Field(..., description="List of notes for the current page")
