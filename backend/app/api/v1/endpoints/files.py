from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_active_user
from app.models.user import User
from app.repositories.note_repository import NoteRepository
from app.schemas.note import NoteResponse

router = APIRouter()


@router.post("/upload/{note_id}", response_model=NoteResponse)
async def upload_file_for_note(
    note_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    note = NoteRepository(db).get_by_id(note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    if note.owner_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to modify this note")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="File is empty")

    return note
