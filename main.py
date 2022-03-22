from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
import crud_user, models, schemas
from database import SessionLocal, engine, get_db
import mongodb_schedule, crud_schedule
from crud_schedule import Participant, create_schedule
from fastapi.security import OAuth2PasswordRequestForm

from security import authenticate_user, create_JWT, get_user

app = FastAPI()


@app.get('/')
async def root():
    return {'message': 'Hello World!'}

@app.post('/user', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud_user.create_user(db=db, user=user)


@app.post('/schedule', response_model=crud_schedule.Schedule)
def create_post(current_user: schemas.User = Depends(get_user)):
    return crud_schedule.create_schedule(owner=current_user.id)

@app.get('/schedules/{schedule_id}', response_model=crud_schedule.Schedule)
def get_schedule(schedule_id, current_user: schemas.User = Depends(get_user)):
    schedule = crud_schedule.get_schedule(schedule_id=schedule_id)
    for participant in schedule.participants:
        if participant.participant_id == current_user.id:
            return schedule
    return {'error': 'Not a participant'}

@app.put('/schedule/{schedule_id}')
def update_schedule(schedule_id: str, participant: Participant, current_user: schemas.User  = Depends(get_user)):
    result = crud_schedule.update_schedule(schedule_id=schedule_id, participant=participant)
    return {'Message': 'Updated'}

@app.post('/token')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user: schemas.User = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_JWT(data={'sub': user.id})
    return {'access_token': access_token, 'token_type': "bearer"}