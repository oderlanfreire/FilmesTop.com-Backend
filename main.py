from fastapi import FastAPI
from user.routers import user_router
from models.userModel import User

from database.database import SessionLocal, engine, Base

Base.metadata.create_all(engine)


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return{'projeto' : 'FilmesTop.com'}

app.include_router(user_router.router)