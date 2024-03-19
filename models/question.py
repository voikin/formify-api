from enum import Enum

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models import Base


class QuestionTypeEnum(Enum):
    single_choice = 'single_choice'
    multiple_choice = 'multiple_choice'
    free_text = 'free_text'


question_type_enum = ENUM('single_choice', 'multiple_choice', 'free_text', name='question_type', create_type=True)


class Question(Base):
    text: Mapped[str]
    type: Mapped[QuestionTypeEnum] = mapped_column(question_type_enum)
    number_in_question: Mapped[int]
    test_id: Mapped[int] = mapped_column(Integer, ForeignKey('tests.id'), nullable=False)

    # Отношения
    test = relationship("Test", back_populates="questions")
    answers = relationship("Answer", back_populates="question")