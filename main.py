from fastapi import FastAPI
from user.routers import user_router
from models.userModel import User

from database.database import engine, Base

Base.metadata.create_all(engine)


app = FastAPI()

@app.get("/")
def read_root():
    return{'projeto' : 'FilmesTop.com'}

app.include_router(user_router.router)