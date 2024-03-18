from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

from models import Base


class Answer(Base):
    text = Column(String, nullable=False)
    is_correct = Column(Boolean, default=False, nullable=False)
    number_in_question = Column(Integer, nullable=False)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)

    # Отношение к вопросам
    question = relationship("Question", back_populates="answers")
