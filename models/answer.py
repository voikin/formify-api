from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models import Base


class Answer(Base):
    text: Mapped[str]
    is_correct: Mapped[bool]
    number_in_question: Mapped[int]
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey('questions.id'), nullable=False)

    # Отношение к вопросам
    question = relationship("Question", back_populates="answers")
