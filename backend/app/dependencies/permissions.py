from collections.abc import Callable

from fastapi import Depends, HTTPException, status

from app.dependencies.auth import get_current_active_user
from app.models.user import User, UserRole


def require_role(allowed_roles: list[UserRole]) -> Callable:
    def role_checker(current_user: User = Depends(get_current_active_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted: Insufficient permissions",
            )
        return current_user

    return role_checker
