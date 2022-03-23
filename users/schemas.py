from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserFull(UserBase):
    hashed_password: str
    id: str
    email_code: str

    class Config:
        orm_mode = True

class User(UserBase):
    id: str

    class Config:
        orm_mode = True