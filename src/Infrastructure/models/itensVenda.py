from sqlalchemy import Column, Integer,  DateTime, ForeignKey, CheckConstraint, UniqueConstraint,DECIMAL

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


from src import db

class ItemVenda(db.Model):
    __tablename__ = 'itens_venda'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    venda_id = Column(Integer, ForeignKey('vendas.id', ondelete='CASCADE'), nullable=False)
    produto_id = Column(Integer, ForeignKey('produtos.id', ondelete='RESTRICT'), nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    # Relacionamentos
    venda = relationship("Venda", back_populates="itens_venda")
    produto = relationship("Produto", back_populates="itens_venda")
    
    # Constraints
    __table_args__ = (
        CheckConstraint('quantidade > 0', name='check_quantidade_positiva'),
        CheckConstraint('preco_unitario >= 0', name='check_preco_positivo'),
        UniqueConstraint('venda_id', 'produto_id', name='uq_venda_produto'),
    )