from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models import Base


class Form(Base):
    title: Mapped[str] = mapped_column(String(255))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))

    # Отношение к вопросам
    questions = relationship("Question", back_populates="form", cascade="all, delete-orphan")
    user = relationship("User", back_populates="forms")
