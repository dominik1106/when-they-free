from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    hashed_password: str
    id: str

    class Config:
        orm_mode = True

class UserLite(UserBase):
    id: str

    class Config:
        orm_mode = True