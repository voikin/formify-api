from datetime import timedelta, datetime
import bcrypt
import jwt
from fastapi import HTTPException
from starlette import status
from configs.config import SingletonSettings
from models import db, User
from repositories.abc_repositories import AbstractUserRepository
from repositories.sqlalchemy.user_repository import UserRepository
from schemas.auth_schemas import TokenInfo

settings = SingletonSettings()


class UserService:
    def __init__(self, user_repo: AbstractUserRepository):
        self.user_repo = user_repo

    async def login_user(self, email: str, password: str) -> TokenInfo:
        unauth_exp = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

        user_from_db = await self.user_repo.get_user_by_email(email)

        if not user_from_db:
            raise unauth_exp

        if not self.verify_password(password, user_from_db.hashed_password):
            raise unauth_exp
        jwt_payload = {"sub": user_from_db.id, "email": user_from_db.email}

        access_token = self.encode_jwt(jwt_payload)
        refresh_token = await self.create_refresh_token(jwt_payload, user_from_db.id)

        return TokenInfo(
            access_token=access_token, refresh_token=refresh_token, token_type="Bearer"
        )

    async def create_user(self, email: str, name: str, password: str) -> TokenInfo:
        user_from_db = await self.user_repo.get_user_by_email(email)

        if user_from_db:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered",
            )

        hashed_password = self.hash_password(password)
        await self.user_repo.create_user(email, name, hashed_password)

        return await self.login_user(email, password)

    async def refresh_access_token(self, refresh_token: str) -> TokenInfo:
        user = await self.user_repo.get_user_by_refresh_token(refresh_token)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )

        payload = self.decode_jwt(refresh_token)

        if datetime.utcfromtimestamp(payload["exp"]) < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token is expired",
            )

        jwt_payload = {"sub": user.id, "email": user.email}

        access_token = self.encode_jwt(jwt_payload)
        refresh_token = await self.create_refresh_token(jwt_payload, user.id)
        return TokenInfo(
            access_token=access_token, refresh_token=refresh_token, token_type="Bearer"
        )

    @staticmethod
    def encode_jwt(
        payload: dict,
        private_key: str = settings.jwt.private_key_path.read_text(),
        algorithm: str = settings.jwt.algorithm,
        expire_minutes: int = settings.jwt.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None,
    ):
        to_encode = payload.copy()
        now = datetime.utcnow()

        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(minutes=expire_minutes)

        to_encode.update(exp=expire, iat=now)

        encoded = jwt.encode(to_encode, private_key, algorithm)

        return encoded

    @staticmethod
    def decode_jwt(
        token: str,
        public_key: str = settings.jwt.public_key_path.read_text(),
        algorithm: str = settings.jwt.algorithm,
    ):
        decoded = jwt.decode(token, public_key, algorithms=[algorithm])

        return decoded

    async def create_refresh_token(self, payload: dict, user_id: int) -> str:
        refresh_token = self.encode_jwt(
            payload=payload, expire_minutes=settings.jwt.refresh_token_expire_minutes
        )
        await self.user_repo.update_refresh_token(user_id, refresh_token)
        return refresh_token

    @staticmethod
    def hash_password(password: str) -> bytes:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt)

    @staticmethod
    def verify_password(password: str, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(password.encode(), hashed_password)


def user_service():
    return UserService(UserRepository(db.session_factory))
