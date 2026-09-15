from fastapi import HTTPException, status

from app.models.note import Note
from app.models.user import User
from app.repositories.note_repository import NoteRepository
from app.schemas.note import NoteCreate, NoteUpdate


class NoteService:
    def __init__(self, note_repo: NoteRepository):
        self.note_repo = note_repo

    def create_note(self, note_in: NoteCreate, current_user: User) -> Note:
        return self.note_repo.create(note_in.title, note_in.content, current_user.id)

    def get_user_notes(self, current_user: User, skip: int = 0, limit: int = 100) -> list[Note]:
        return self.note_repo.get_by_user(current_user.id, skip=skip, limit=limit)

    def get_note_for_user(self, note_id: int, current_user: User) -> Note:
        note = self.note_repo.get_by_id(note_id)
        if note is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
        if note.owner_id != current_user.id and current_user.role.value != "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this note")
        return note

    def update_note(self, note_id: int, note_in: NoteUpdate, current_user: User) -> Note:
        note = self.note_repo.get_by_id(note_id)
        if note is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
        if note.owner_id != current_user.id and current_user.role.value != "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this note")
        return self.note_repo.update(note, title=note_in.title, content=note_in.content)

    def delete_note(self, note_id: int, current_user: User) -> Note:
        note = self.note_repo.get_by_id(note_id)
        if note is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
        if note.owner_id != current_user.id and current_user.role.value != "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this note")
        return self.note_repo.delete(note)
