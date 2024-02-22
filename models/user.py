from sqlalchemy import Column, String, LargeBinary
from models.base import Base


class User(Base):
    email = Column(String, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(LargeBinary, nullable=False)
    refresh_token = Column(String, nullable=True)
