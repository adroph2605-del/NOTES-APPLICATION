from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.permissions import require_role
from app.models.user import User, UserRole
from app.repositories.user_repository import UserRepository

router = APIRouter()


@router.get("/users", response_model=list[dict])
async def list_users(
    db: Session = Depends(get_db),
    _: User = Depends(require_role([UserRole.ADMIN])),
):
    users = UserRepository(db).get_all()
    return [{"id": user.id, "email": user.email, "role": user.role.value} for user in users]
