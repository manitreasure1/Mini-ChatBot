from fastapi import APIRouter, status, Depends, Response, Cookie
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Optional
from ..db.schemas import CreateUser, LoginUser, UserResponse
from ..services.auth_service import AuthService
from ..db.database import get_session


auth_service = AuthService()
router = APIRouter(tags=["Authentication"])


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse
)
async def register(new_user: CreateUser, session: AsyncSession = Depends(get_session)):
    user = await auth_service.register_user(new_user, session)
    return user


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    user_credentials: LoginUser,
    response: Response,
    session: AsyncSession = Depends(get_session),
):
    result = await auth_service.login_user(user_credentials, session, response)
    return result


@router.post("/refresh-token", status_code=status.HTTP_200_OK)
async def refresh_token(
    response: Response, refresh_token: Optional[str] = Cookie(None)
):
    result = await auth_service.refresh_token(response, refresh_token)
    return result


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(response: Response):
    result = auth_service.logout(response)
    return result
