from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    hashed_password: str
    uuid: str

    class Config:
        orm_mode = True