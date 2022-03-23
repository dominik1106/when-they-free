from typing import List
from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from users.database import get_db
import users.crud, users.schemas
from users.models import Base
from users.database import engine
import schedules.crud, schedules.schemas
from fastapi.security import OAuth2PasswordRequestForm
from security import authenticate_user, create_JWT, get_user
from .email import send_confirmation_email

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get('/')
async def root():
    return {'message': 'Hello World!'}


@app.post('/schedule', response_model=schedules.crud.Schedule)
def create_post(current_user: users.schemas.User = Depends(get_user)):
    return schedules.crud.create_schedule(owner=current_user.id)

@app.get('/schedules/{schedule_id}', response_model=schedules.crud.Schedule)
def get_schedule(schedule_id, current_user: users.schemas.User = Depends(get_user)):
    schedule = schedules.crud.get_schedule(schedule_id=schedule_id)
    for participant in schedule.participants:
        if participant.participant_id == current_user.id:
            return schedule
    return {'error': 'Not a participant'}

# TODO just pass the busy times as a array, convert them to timeframes, use current_user
@app.put('/schedule/{schedule_id}', response_model=schedules.crud.Schedule)
def update_schedule(schedule_id: str, busy_times: List[schedules.schemas.TimeFrame], current_user: users.schemas.User  = Depends(get_user)):
    return schedules.crud.update_schedule(schedule_id, busy_times, current_user.id)

@app.post('/token')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user: users.schemas.User = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_JWT(data={'sub': user.id})
    return {'access_token': access_token, 'token_type': "bearer"}


@app.post('/user', response_model=users.schemas.User)
def create_user(user: users.schemas.UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    _user =  users.crud.create_user(db=db, user=user)
    background_tasks.add_task(send_confirmation_email(_user.email, _user.email_hash))
    return _user

@app.get('/verify/{hash}')
def verify_email(hash: str, db: Session = Depends(get_db)):
    user = users.crud.get_user_by_email_hash(db, hash)
    if not user:
        return 'Error'

    users.crud.activate_user(db, user.id)

    return 'Success'

# I SHOULD change the email hash everytime, but it is just insecure random characters anyway so fuck it
@app.get('/resend')
async def resend_email_code(email: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user = users.crud.get_user_by_email(db, email)
    if not user:
        return 'Error'
    background_tasks.add_task(send_confirmation_email(email, user.email_hash))
    return 'Success'