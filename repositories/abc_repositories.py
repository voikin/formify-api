from abc import ABC, abstractmethod
from typing import Optional, List

from models import User, Form
from schemas.form_schemas import QuestionSchema


class AbstractUserRepository(ABC):
    @abstractmethod
    async def create_user(
        self, email: str, name: str, hashed_password: bytes
    ) -> Optional[User]:
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


class AbstractFormRepository(ABC):
    @abstractmethod
    async def get_tests_by_user_id(self, user_id: int) -> Optional[List[Form]]:
        raise NotImplementedError()

    @abstractmethod
    async def get_test_by_id(self, test_id: int) -> Optional[List[Form]]:
        raise NotImplementedError()

    @abstractmethod
    async def create_test(self, title: str, user_id: int, questions: List[QuestionSchema]) -> int:
        raise NotImplementedError()

    @abstractmethod
    async def get_right_answers(self, form_id: int):
        raise NotImplementedError()

    @abstractmethod
    async def delete_form(self, form_id: int):
        raise NotImplementedError()

    @abstractmethod
    async def get_user_by_form_id(self, form_id: int) -> User:
        raise NotImplementedError()

    @abstractmethod
    async def update_form(self, form_id: int, form_title: str, questions: List[QuestionSchema]):
        raise NotImplementedError()
