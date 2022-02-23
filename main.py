from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
import crud_user, models, schemas
from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try: 
        yield db
    #TODO Except: Error handling
    finally:
        db.close()


@app.get('/')
async def root():
    return {'message': 'Hello World!'}

@app.post('/create-user')
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud_user.create_user(db=db, user=user)