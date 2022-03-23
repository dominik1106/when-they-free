from sqlalchemy.orm import Session
from uuid import uuid4
from passlib.context import CryptContext
from . import models, schemas
import string, random

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password):
    return pwd_context.hash(password)


def get_user(db: Session, uuid: str) -> models.User:
    return db.query(models.User).filter(models.User.id == uuid).first()

def get_user_by_email(db: Session, email: str) -> models.User:
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_email_hash(db: Session, hash: str) -> models.User:
    return db.query(models.User).filter(models.User.email_hash == hash).first()

def create_user(db: Session, user: schemas.UserCreate):
    #TODO: Password hash implementation
    hsh_pwd = hash_password(user.password)
    email_hsh = ''.join(random.choices(string.ascii_uppercase + string.digits, k=32))
    uuid_4 = uuid4().hex
    
    db_user = models.User(email=user.email, id=uuid_4, hashed_password=hsh_pwd, email_hash=email_hsh)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
    return schemas.UserFull(email=db_user.email, id=db_user.id)

def activate_user(db: Session, uuid: str):
    user = get_user(db, uuid)
    setattr(user, 'activated', True)
    db.add(user)
    db.commit()
    db.refresh(user)