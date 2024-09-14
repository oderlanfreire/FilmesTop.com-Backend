from database.database import Base
from sqlalchemy import  Column, VARCHAR, Integer, Text


class Filmes(Base):
    __tablename__ = 'filmes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    Nome = Column(VARCHAR(50))
    Genero = Column(VARCHAR(50))
    Ano = Column(Integer)
    Sinopse = Column(Text)
    Diretor = Column(VARCHAR(50))

