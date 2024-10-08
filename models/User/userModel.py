import uuid
from sqlalchemy import  Column, VARCHAR, JSON
import phonenumbers
from database.database import Base

def gerar_uuid():
    return str(uuid.uuid4())
class User(Base):
    __tablename__ = "usuario"

    id = Column(VARCHAR(36), primary_key=True, default=gerar_uuid)
    nome = Column(VARCHAR(50), nullable= False)
    email = Column(VARCHAR(50), nullable= False)
    telefone = Column(VARCHAR(50), nullable= False)
    filmes_alugados = Column(JSON, nullable= True)

    @property
    def formatar_numero(self):
        if self.telefone:
            tel = phonenumbers.parse(self.telefone, None)
            return phonenumbers.format_number(tel, phonenumbers.PhoneNumberFormat.E164)

