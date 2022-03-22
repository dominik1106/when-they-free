from sqlalchemy.orm import Session
from uuid import uuid4
from passlib.context import CryptContext
from . import models, schemas

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
def hash_password(password):
    return pwd_context.hash(password)


def get_user(db: Session, uuid: str):
    return db.query(models.User).filter(models.User.id == uuid).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    #TODO: Password hash implementation
    hsh_pwd = hash_password(user.password)
    uuid_4 = uuid4().hex
    
    db_user = models.User(email=user.email, id=uuid_4, hashed_password=hsh_pwd)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return schemas.User(email=db_user.email, id=db_user.id)