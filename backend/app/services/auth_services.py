from fastapi import HTTPException, status

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserLogin


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register_user(self, user_in: UserCreate) -> User:
        existing_user = self.user_repo.get_by_email(user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already registered",
            )

        hashed_password = hash_password(user_in.password)
        return self.user_repo.create(user_in, hashed_password)

    def authenticate_user(self, credentials: UserLogin) -> User:
        user = self.user_repo.get_by_email(credentials.email)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="wrong email")
        if not verify_password(credentials.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="wrong password")
        return user

    def create_user_token(self, user: User) -> dict:
        token = create_access_token({"sub": user.email})
        return {"access_token": token, "token_type": "bearer"}
