from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from database.dependency import get_db
from models.User.userModel import User
from models.Filmes.filmesModel import Filmes
import json



async def register_user(user, db: Session = Depends(get_db)):
    usuario = User(
        nome= user.nome,
        email= user.email,
        telefone= user.telefone
    )
    try:
        usuario_ja_cadastrado = db.query(User).filter(User.email == user.email).first()
        if usuario_ja_cadastrado:
            raise HTTPException(status_code=status.HTTP_302_FOUND, detail=str("Usuário já está cadastrado."))
        else:
            db.add(usuario)
            db.commit()
            db.refresh(usuario)
            
            return "usuario cadastrado com sucesso."
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
async def movie_list(db: Session = Depends(get_db)):
    try:
        filmes_db = db.query(Filmes).all()
        filmes = []
        for filme in filmes_db:
            filmes.append(filme.Nome)
        return filmes
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

async def movie_list_by_gender(genero: str, db: Session  = Depends(get_db)):
    try:
        filmes_por_genero = []
        filmes_db = db.query(Filmes)
        for filme in filmes_db:
            if filme.Genero == genero.capitalize():
                filmes_por_genero.append(filme.Nome)
        if len(filmes_por_genero) == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Gênero não disponível no momento.")

        return filmes_por_genero
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

async def movie_data(titulo: str, db: Session = Depends(get_db)):
    try:
        filme = db.query(Filmes).filter(Filmes.Nome == titulo.capitalize()).first()
        if not filme:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O filme não está disponível no catálogo.")
        
        return filme
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= str(e))
    
async def rent_movie(cliente_email: str, titulo: str, db: Session = Depends(get_db)):
    try:
        usuario = db.query(User).filter(User.email == cliente_email).first()
        if not usuario:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuário não encontrado.")
        
        filme = db.query(Filmes).filter(Filmes.Nome == titulo.capitalize()).first()
        if not filme:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O filme não está disponível no catálogo.")
        
        if not usuario.filmes_alugados:
            usuario.filmes_alugados = []
        else:
            if isinstance(usuario.filmes_alugados, str):
                usuario.filmes_alugados = json.loads(usuario.filmes_alugados)


        aluguel = {"Nome" : filme.Nome}
        if aluguel not in usuario.filmes_alugados:
            usuario.filmes_alugados.append(aluguel)
        else:
            raise Exception(status_code= status.HTTP_400_BAD_REQUEST, detail="Filme já alugado.")
        
        usuario.filmes_alugados = json.dumps(usuario.filmes_alugados)

        
        db.commit()
        db.refresh(usuario)
        return {"message" : "Filme alugado com sucesso."}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    

async def rate_movie(titulo: str, nota: float, cliente_email: str, db: Session = Depends(get_db)):
    try:
        nota_filmes = 0
        titulo = titulo
        nota = round(nota, 1)
        if nota < 1 or nota > 5 :
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nota inválida, insira uma nota entre 1 e 5")
        
        usuario = db.query(User).filter(User.email == cliente_email).first()
        if not usuario:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuário não encontrado.")
        filmes_alugados = json.loads(usuario.filmes_alugados)

        usuarios = db.query(User)
        filme_catalogo = db.query(Filmes).filter(Filmes.Nome == titulo.capitalize()).first()
        if filme_catalogo.total_avaliacoes == None:
            filme_catalogo.total_avaliacoes = 0


        alugou = False
        for filme in filmes_alugados:
            if isinstance(filme, dict) and filme.get("Nome") == titulo:
                if filme.get("Nota") is not None and filme["Nota"]:
                    filme["Nota"] = nota
                    alugou = True
                    break
                else:
                    filme["Nota"] = nota
                    alugou = True
                    filme_catalogo.total_avaliacoes = filme_catalogo.total_avaliacoes + 1
                    break
        if not alugou:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"O {titulo} ainda não foi alugado.")
        usuario.filmes_alugados = json.dumps(filmes_alugados)

        for usr in usuarios:
            filmes_usr = json.loads(usr.filmes_alugados)
            for filme in filmes_usr:
                if isinstance(filme, dict) and filme.get("Nome") == titulo:
                    if filme.get("Nota") is not None:
                        nota_filmes = nota_filmes + filme["Nota"]

        filme_catalogo.nota_final = nota_filmes / filme_catalogo.total_avaliacoes
        
        db.commit()
        db.refresh(usuario)
        db.refresh(filme_catalogo)
        return {"message" : "Nota registrada com sucesso."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

async def rented_movies(cliente_email: str, db: Session = Depends(get_db)):
    try:

        usuario = db.query(User).filter(User.email == cliente_email).first()
        filmes = json.loads(usuario.filmes_alugados)
        return filmes
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
