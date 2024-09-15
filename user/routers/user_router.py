from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database.dependency import get_db
from models.User.userModel import User
from models.Filmes.filmesModel import Filmes
from controllers.User.userController import *
import json


router = APIRouter(prefix="/user")

class UserRegister(BaseModel):
    nome: str
    email: str
    telefone: str


@router.post('/register-user', status_code= status.HTTP_201_CREATED)
async def create_user(user:UserRegister, db: Session = Depends(get_db)):
    return await register_user(user, db)

    

@router.get('/listar-filmes/', status_code=status.HTTP_200_OK)
async def get_movie_list(db: Session = Depends(get_db)):
    return await movie_list(db)

@router.get('/listar-genero/{genero}', status_code= status.HTTP_200_OK )
async def get_movie_list_by_gender(genero: str, db: Session  = Depends(get_db)):
   return await movie_list_by_gender(genero, db)



@router.get('/filme/{titulo}', status_code= status.HTTP_200_OK)
async def get_movie_data(titulo: str, db: Session = Depends(get_db)):
    return await movie_data(titulo, db)

@router.post('/alugar-filme', status_code= status.HTTP_201_CREATED)
async def do_rent_movie(cliente_email: str, titulo: str, db: Session = Depends(get_db)):
    return await rent_movie(cliente_email, titulo, db)

@router.post('/avaliar-filme', status_code=status.HTTP_201_CREATED)
async def do_rate_movie(titulo: str, nota: float, cliente_email: str, db: Session = Depends(get_db)):
    return await rate_movie(titulo, nota, cliente_email, db)


@router.get('/filmes-alugados/{cliente_email}', status_code=status.HTTP_200_OK)
async def get_rented_movies(cliente_email: str, db: Session = Depends(get_db)):
    return await rented_movies(cliente_email, db)
