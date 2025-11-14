from src import db
from sqlalchemy import Integer, Column, String

class Admin(db.Model):
    __tablename__ = "admin"
    
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, nullable=False)
    email = Column(String, nullable=False)
    celular = Column(String, nullable=False)
    senha = Column(String, nullable=False)
