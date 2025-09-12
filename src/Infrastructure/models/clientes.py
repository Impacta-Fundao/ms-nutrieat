from src import db
from sqlalchemy import Integer, Column, String, Date

class Cliente(db.Model):
    __tablename__ = "clientes"
    
    id = (Column(Integer, primary_key=True))
    nome = (Column(String(255), nullable=False))
    cpf = (Column(String(255), nullable=False))
    data_nascimento = (Column(Date, nullable=False))
    
    @property
    def data_nascimento_formatada(self):
        return self.data_nascimento.isoformat() if self.data_nascimento else None
    
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cpf": self.cpf,
            "data_nascimento": self.data_nascimento.isoformat()
        }