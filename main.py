from fastapi import FastAPI
from user.routers import user_router
from models.User.userModel import User




app = FastAPI()


app.include_router(user_router.router)