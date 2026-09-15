from sqlalchemy.orm import Session

from app.models.note import Note


class NoteRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, title: str, content: str, owner_id: int) -> Note:
        note = Note(title=title, content=content, owner_id=owner_id)
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        return note

    def get_by_id(self, note_id: int) -> Note | None:
        return self.db.query(Note).filter(Note.id == note_id).first()

    def get_by_user(self, owner_id: int, skip: int = 0, limit: int = 100) -> list[Note]:
        return self.db.query(Note).filter(Note.owner_id == owner_id).offset(skip).limit(limit).all()

    def update(self, note: Note, title: str | None = None, content: str | None = None) -> Note:
        if title is not None:
            note.title = title
        if content is not None:
            note.content = content
        self.db.commit()
        self.db.refresh(note)
        return note

    def delete(self, note: Note) -> Note:
        self.db.delete(note)
        self.db.commit()
        return note
