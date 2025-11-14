from src import db
from sqlalchemy import Integer, Column, String, Date

class Cliente(db.Model):
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, nullable=False)
    data_nascimento = Column(Date, nullable=False)
    turno = Column(String, nullable=False)
    sala = Column(String, nullable=False)
    numero = Column(String, nullable=False)
    email = Column(String, nullable=False)
