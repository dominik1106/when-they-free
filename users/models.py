from sqlalchemy import Boolean, Column, Integer, String

from .database import Base
from uuid import uuid4

class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True, index=True, default=uuid4)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)