import os
from dotenv import load_dotenv
from typing import Optional
from pydantic import BaseModel
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from passlib.context import CryptContext
from jose import JWTError, jwt

import crud_user
from sqlalchemy.orm import Session
from database import get_db

load_dotenv()
JWT_SECRET = os.environ.get('JWT_SECRET')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')



class TokenData(BaseModel):
    user_id: Optional[str] = None


### PASSWORD UTILITY FUNCTIONS
def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def hash_password(password):
    return pwd_context.hash(password)


### LOGIN
# First confirm that User has account & password is correct
def authenticate_user(db, email: str, password: str):
    user = crud_user.get_user_by_email(db=db, email=email)
    if user is None:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Then generate a JWT token which contains the uuid and is valid for ACCESS_TOKEN_EXPIRE_MINUTES (30)
def create_JWT(data: dict, expires_delta: Optional[int] = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()

    expire = datetime.utcnow() + expires_delta
    to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt



### ROUTE SECURITY
# Called whenever secured Route
# Also provides information such as email & uuid about current user
async def get_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        user_id: str = payload.get('sub')
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    user = crud_user.get_user(db=db, uuid=token_data.user_id)
    if user is None:
        raise credentials_exception

    return user