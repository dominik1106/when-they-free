from sqlalchemy.orm import Session
import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_mongoid(db: Session, mongo_id: bytes):
    return db.query(models.User).filter(models.User.mongo_id == mongo_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    #TODO: Password hash implementation
    hsh_pwd = user.password + 'Bcrypt Hash'
    db_user = models.User(email=user.email, mongo_id=user.mongo_id, hashed_password=hsh_pwd)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user #Prob exclude the pwd here