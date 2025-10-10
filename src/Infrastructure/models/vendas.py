from src import db
from sqlalchemy import Integer, Column, DateTime, ForeignKey, DECIMAL, Enum as SQLAlchemyEnum
import enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class FormaPagamento(enum.Enum):
    DINHEIRO = "dinheiro"
    CARTAO_CREDITO = "cartao_credito"
    CARTAO_DEBITO = "cartao_debito"
    PIX = "pix"

class StatusPagamento(enum.Enum):
    PENDENTE = "pendente"
    PAGO = "pago"
    CANCELADO = "cancelado"

class Vendas(db.Model):
    __tablename__ = "vendas"
    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id', ondelete='RESTRICT'), nullable=False)
    data_venda = Column(DateTime, default=func.now())
    valor_total = Column(DECIMAL(10,2), nullable=False, default=0.00)
    status_pagamento = Column(SQLAlchemyEnum(StatusPagamento), default=StatusPagamento.PENDENTE)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    forma_pagamento = Column(SQLAlchemyEnum(FormaPagamento), default=FormaPagamento.DINHEIRO)
    cliente = relationship("Cliente", backref="vendas")
    # itens_venda = relationship("ItemVenda", back_populates="venda", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            "id" : self .id,
            "cliente_id" : self.cliente_id, 
            "data_venda" : self.data_venda,
            "valor_total" : self.valor_total,
            "status_pagamento" : self.status_pagamento,
            "created_at" : self.created_at,
            "updated_at" : self.updated_at,
            "forma_pagamento" : self.forma_pagamento,
            "cliente" : self.cliente,
            "itens_venda" : self.itens_venda
        }
    