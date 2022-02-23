from sqlalchemy.orm import Session
import models, schemas
from uuid import uuid4


def get_user(db: Session, uuid: str):
    return db.query(models.User).filter(models.User.id == uuid).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    #TODO: Password hash implementation
    hsh_pwd = user.password + 'Bcrypt Hash'
    uuid_4 = uuid4().hex
    
    db_user = models.User(email=user.email, id=uuid_4, hashed_password=hsh_pwd)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return schemas.User(email=db_user.email, id=db_user.id)