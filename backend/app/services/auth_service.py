from sqlmodel.ext.asyncio.session import AsyncSession
from ..db.schemas import CreateUser, LoginUser
from passlib.context import CryptContext
from datetime import datetime, timedelta
from .user_service import UserService
from ..config.env import EnvConfig
from ..db.models import Users
import jwt
from app.db.database import get_session
from typing import  Optional
from fastapi.security import (
    OAuth2PasswordBearer,
    HTTPBearer,
)
from fastapi import Response, Cookie, HTTPException, Depends, status

security = HTTPBearer(auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
env_config = EnvConfig() # type: ignore
user_service = UserService()


class AuthService:
    async def register_user(self, new_user: CreateUser, session: AsyncSession):
        ex_user = await user_service.get_user_by_email(
            new_user.email, session, raise_on_not_found=False
        )
        if ex_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists",
            )

        hashed_password = self.hash_password(new_user.password)
        create_new_user = Users(
            firstname=new_user.firstname,
            lastname=new_user.lastname,
            email=new_user.email,
            username=new_user.email.split("@")[0],
            password_hash=hashed_password,
        )
        session.add(create_new_user)
        await session.commit()
        await session.refresh(create_new_user)
        return create_new_user

    async def login_user(
        self, user: LoginUser, session: AsyncSession, response: Response
    ):
        login_user = await user_service.get_user_by_email(user.email, session)
        if login_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        if not self.verify_password(user.password, login_user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        payload = {"sub": login_user.username, "email": login_user.email}

        access_token = self.create_access_token(user_data=payload)
        refresh_token = self.create_refresh_token(user_data=payload)

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=env_config.ACCESS_TOKEN_EXPIRES * 60,
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=env_config.REFRESH_TOKEN_EXPIRES * 24 * 60 * 60,
        )
        return {"message": "Login successful", "username": login_user.username}

    async def refresh_token(
        self, response: Response, refresh_token: Optional[str] = Cookie(None)
    ):
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token not found",
            )
        try:
            payload = self.decode_token(refresh_token)
            if not payload.get("refresh"):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token",
                )

            username = payload.get("sub")
            email = payload.get("email")

            if not username or not email:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token payload",
                )
            new_payload = {"sub": username, "email": email}

            new_access_token = self.create_access_token(new_payload)
            response.set_cookie(
                key="access_token",
                value=new_access_token,
                httponly=True,
                secure=True,
                samesite="lax",
                max_age=env_config.ACCESS_TOKEN_EXPIRES * 60,
            )
            return {"message": "Token refreshed successfully"}

        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    def logout(self, response: Response):
        response.delete_cookie(key="access_token")
        response.delete_cookie(key="refresh_token")
        return {"message": "Logged out successfully"}


    async def get_current_user(self, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = self.decode_token(token)
            email = payload.get("email")
            if not email:
                raise credentials_exception

            user = await user_service.get_user_by_email(email, session)
            if not user:
                raise credentials_exception

            return user
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, ValueError):
            raise credentials_exception

    # async def get_token(
    #     self,
    #     credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    #     access_token: Optional[str] = Cookie(None),
    # ) -> str:
    #     if credentials:
    #         return credentials.credentials
    #     if access_token:
    #         return access_token
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Not authenticated",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(user_data: dict) -> str:
        to_encode = user_data.copy()
        expire = datetime.now() + timedelta(minutes=env_config.ACCESS_TOKEN_EXPIRES)
        to_encode.update(
            {
                "exp": expire,
                "refresh": False,
                "iat": datetime.now(),
            }
        )
        encoded_jwt = jwt.encode(
            to_encode, env_config.SECRET_KEY, algorithm=env_config.ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    def create_refresh_token(user_data: dict) -> str:
        to_encode = user_data.copy()
        expire = datetime.utcnow() + timedelta(days=env_config.REFRESH_TOKEN_EXPIRES)
        to_encode.update(
            {
                "exp": expire,
                "refresh": True,
                "iat": datetime.now(),
            }
        )
        encoded_jwt = jwt.encode(
            to_encode, env_config.SECRET_KEY, algorithm=env_config.ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            payload = jwt.decode(
                jwt=token, key=env_config.SECRET_KEY, algorithms=[env_config.ALGORITHM]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired. Please login again.")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")
