from typing import Optional

from sqlalchemy import Column, String, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class User(Base):
    email: Mapped[str]
    name: Mapped[str]
    hashed_password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    refresh_token: Mapped[Optional[str]]

    tests = relationship("Test", back_populates="user")
