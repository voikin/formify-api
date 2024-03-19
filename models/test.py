from typing import Optional

from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models import Base


class Test(Base):
    title: Mapped[str]
    description: Mapped[Optional[str]]
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))

    # Отношение к вопросам
    questions = relationship("Question", back_populates="test")
    user = relationship("User", back_populates="tests")
