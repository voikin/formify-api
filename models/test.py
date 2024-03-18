from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models import Base


class Test(Base):
    title = Column(String, nullable=False)
    description = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Отношение к вопросам
    questions = relationship("Question", back_populates="test")
    user = relationship("User", back_populates="tests")