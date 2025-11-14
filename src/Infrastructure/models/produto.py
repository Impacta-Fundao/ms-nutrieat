from src import db
from sqlalchemy import Integer, Column, String, NUMERIC

class Produto(db.Model):
    __tablename__ = "produto"
    
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    preco = Column(NUMERIC(10, 2), nullable=False)
