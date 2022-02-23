from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Binary

from .database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    mongo_id = Column(Binary, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)