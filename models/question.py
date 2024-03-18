from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship

from models import Base


question_type_enum = ENUM('single_choice', 'multiple_choice', 'free_text', name='question_type', create_type=True)


class Question(Base):
    text = Column(String, nullable=False)
    type = Column(question_type_enum, nullable=False)
    number_in_question = Column(Integer, nullable=False)
    test_id = Column(Integer, ForeignKey('tests.id'), nullable=False)

    # Отношения
    test = relationship("Test", back_populates="questions")
    answers = relationship("Answer", back_populates="question")