from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID
from ..db.models import Users
from ..db.schemas import UpdateUser, CurrentUser
from pydantic import EmailStr
from sqlmodel import select
from fastapi import HTTPException, status
from typing import Optional, Sequence


class UserService:
    async def update_user_profile(
        self, current_user: CurrentUser, user_data: UpdateUser, session: AsyncSession
    ) -> Users:
        user = await self.get_user_by_email(current_user.email, session)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        update_data = user_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)

        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    async def get_user_by_id(self, user_id: UUID, session: AsyncSession) -> Users:
        user = await session.get(Users, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user

    async def get_user_by_email(
        self, email: EmailStr, session: AsyncSession, raise_on_not_found: bool = False
    ) -> Users | None:

        statement = select(Users).where(Users.email == email)
        result = await session.exec(statement)
        user = result.first()

        if not user and raise_on_not_found:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return user

    async def check_user_exists(self, email: EmailStr, session: AsyncSession) -> bool:
        user = await self.get_user_by_email(email, session, raise_on_not_found=False)
        return user is not None

    async def get_all_users(
        self, session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> Sequence[Users]:
        statement = select(Users).offset(skip).limit(limit)
        result = await session.exec(statement)
        return result.all()

    async def delete_user(self, user_id: UUID, session: AsyncSession) -> dict:
        user = await self.get_user_by_id(user_id, session)
        await session.delete(user)
        await session.commit()
        return {"message": "User deleted successfully"}
