from typing import Optional
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
import crud_user, models, schemas
from database import SessionLocal, engine
import mongodb_schedule, crud_schedule
from crud_schedule import Participant, create_schedule


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

@app.post('/create-user', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud_user.create_user(db=db, user=user)


@app.get('/schedules/{schedule_id}', response_model=crud_schedule.Schedule)
def get_schedule(schedule_id):
    return crud_schedule.get_schedule(schedule_id=schedule_id)

@app.post('/create-schedule', response_model=crud_schedule.Schedule)
def create_post(owner: str):
    return crud_schedule.create_schedule(owner=owner)