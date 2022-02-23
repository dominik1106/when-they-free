from fastapi import FastAPI
import user_crud, models, schemas
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