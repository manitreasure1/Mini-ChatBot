
from fastapi import APIRouter, Depends
from app.db.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.schemas import UserOut, UpdateUser
from app.services.user_service import UserService
from app.services.auth_service import AuthService

router = APIRouter(tags=["User"])
user_service =UserService()
auth_service =AuthService()


@router.get("/profile", response_model=UserOut)
async def get_user_profile(current_user=Depends(auth_service.get_current_user)):
    return current_user


@router.patch("/profile", response_model=UserOut)
async def update_user_profile(
    user_data: UpdateUser,
    current_user=Depends(auth_service.get_current_user),
    session: AsyncSession = Depends(get_session),
):
    updated_user = await user_service.update_user_profile(
        current_user=current_user, user_data=user_data, session=session
    )
    return updated_user
