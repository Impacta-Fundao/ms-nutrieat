from src import db
from sqlalchemy import Column, Integer, Numeric, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum


class FormaPagamento(enum.Enum):
    cartao_credito = "cartao_credito"
    cartao_debito = "cartao_debito"
    pix = "pix"
    dinheiro = "dinheiro"
    
class StatusPagamento(enum.Enum):
    pago = "pago"
    pendente = "pendente"
    cancelado = "cancelado"

class Vendas(db.Model):
    __tablename__ = 'vendas'
    
    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    data_venda = Column(DateTime, nullable=False)
    valor_total = Column(Numeric(10,2), nullable=True)
    status_pagamento = Column(Enum(StatusPagamento), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    forma_pagamento = Column(Enum(FormaPagamento), nullable=False)
    