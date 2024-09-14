import uuid
from sqlalchemy import  Column, VARCHAR
import phonenumbers
from database.database import Base

class User(Base):
    __tablename__ = "usuario"

    id = Column(VARCHAR(36), primary_key=True, default=str(uuid.uuid4()))
    nome = Column(VARCHAR(50))
    email = Column(VARCHAR(50))
    telefone = Column(VARCHAR(50))

    @property
    def formatar_numero(self):
        if self.telefone:
            tel = phonenumbers.parse(self.telefone, None)
            return phonenumbers.format_number(tel, phonenumbers.PhoneNumberFormat.E164)


