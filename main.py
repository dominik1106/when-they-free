from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from users.database import get_db
import users.crud, users.schemas
import schedules.crud
from fastapi.security import OAuth2PasswordRequestForm
from security import authenticate_user, create_JWT, get_user

app = FastAPI()


@app.get('/')
async def root():
    return {'message': 'Hello World!'}

@app.post('/user', response_model=users.schemas.User)
def create_user(user: users.schemas.UserCreate, db: Session = Depends(get_db)):
    return users.crud.create_user(db=db, user=user)


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

@app.put('/schedule/{schedule_id}')
def update_schedule(schedule_id: str, participant: schedules.crud.Participant, current_user: users.schemas.User  = Depends(get_user)):
    result = schedules.crud.update_schedule(schedule_id=schedule_id, participant=participant)
    return {'Message': 'Updated'}

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