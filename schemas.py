from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    mongo_id: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    hsh_password: str

    class Config:
        orm_mode = True