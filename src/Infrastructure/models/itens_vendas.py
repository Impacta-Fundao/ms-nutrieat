from src import db
from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey

class ItensVendas(db.Model):
    __tablename__ = 'itens_venda'
    
    id = Column(Integer, primary_key=True)
    venda_id = Column(Integer, ForeignKey('vendas.id'), nullable=False)
    produto_id = Column(Integer, ForeignKey('produto.id'), nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Numeric(10,2), nullable=True)
    created_at = Column(DateTime, nullable=False)
