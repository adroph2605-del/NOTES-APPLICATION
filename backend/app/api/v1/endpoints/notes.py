from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_active_user
from app.models.user import User
from app.repositories.note_repository import NoteRepository
from app.schemas.note import NoteCreate, NoteResponse, NoteUpdate
from app.services.note_services import NoteService

router = APIRouter()


@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(
    note_in: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    note_repo = NoteRepository(db)
    note_service = NoteService(note_repo)
    return note_service.create_note(note_in, current_user)


@router.get("/", response_model=list[NoteResponse])
def get_notes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    note_repo = NoteRepository(db)
    note_service = NoteService(note_repo)
    return note_service.get_user_notes(current_user, skip=skip, limit=limit)


@router.get("/{note_id}", response_model=NoteResponse)
def get_single_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    note_repo = NoteRepository(db)
    note_service = NoteService(note_repo)
    return note_service.get_note_for_user(note_id, current_user)


@router.patch("/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    note_in: NoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    note_repo = NoteRepository(db)
    note_service = NoteService(note_repo)
    return note_service.update_note(note_id, note_in, current_user)


@router.delete("/{note_id}", response_model=NoteResponse)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    note_repo = NoteRepository(db)
    note_service = NoteService(note_repo)
    return note_service.delete_note(note_id, current_user)
