from abc import ABC, abstractmethod
from typing import Optional

from models import User


class AbstractUserRepository(ABC):
    @abstractmethod
    async def create_user(self, email: str, name: str, hashed_password: bytes) -> Optional[User]:
        raise NotImplementedError()

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError()

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        raise NotImplementedError()

    @abstractmethod
    async def update_refresh_token(self, user_id: int, refresh_token: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_user_by_refresh_token(self, refresh_token: str) -> Optional[User]:
        raise NotImplementedError()
