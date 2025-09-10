from src import db
from sqlalchemy import Integer, Column, String,NUMERIC, Date

class Cliente(db.Model):
    __tablename__ = "cliente"
    
    id = (Column(Integer, primary_key=True))
    nome = (Column(String(255), nullable=False))
    cpf = (Column(String(255), nullable=False))
    data_nascimento = (Column(Date))
    
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cpf": self.cpf,
            "data_nascimento": self.data_nascimento
        }