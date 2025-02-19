from enum import Enum
from typing import List
from fastapi import HTTPException, Depends, status
from models.user import User
from routers.auth import get_current_user

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class RoleChecker:
    def __init__(self, allowed_roles: List[UserRole]):
        self.allowed_roles = allowed_roles

    async def __call__(self, user: User = Depends(get_current_user)):
        if UserRole(user.role) not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="У вас недостаточно прав для выполнения этой операции"
            )
        return user

# Создаем проверки для разных ролей
admin_required = RoleChecker([UserRole.ADMIN])