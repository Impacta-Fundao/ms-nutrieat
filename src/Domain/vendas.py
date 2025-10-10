from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from enum import Enum
from src.Domain.cliente import ClientDomain

class StatusPagamento(Enum):
    PENDENTE = "pendente"
    PAGO = "pago"
    CANCELADO = "cancelado"

class FormaPagamento(Enum):
    DINHEIRO = "dinheiro"
    CARTAO_CREDITO = "cartao_credito"
    CARTAO_DEBITO = "cartao_debito"
    PIX = "pix"

class ItemVendaDomain:
    def __init__(self, produto_id: int, quantidade: int, preco_unitario: Decimal):
        self.produto_id = produto_id
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
        
class VendaDomain:
    def __init__(
        self,
        cliente_id: int,
        itens_venda: List[ItemVendaDomain],
        status_pagamento: StatusPagamento = StatusPagamento.PENDENTE,
        forma_pagamento: Optional[FormaPagamento] = FormaPagamento.DINHEIRO,
        data_venda: Optional[datetime] = None,
        valor_total : Optional[Decimal] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        id:Optional[int]  = None
          
    ):
        self.id = id
        self.cliente_id = cliente_id
        self.data_venda = data_venda or datetime.now()
        self.valor_total = valor_total
        self._itens_venda = itens_venda
        self.status_pagamento = status_pagamento
        self.forma_pagamento = forma_pagamento
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        
        

   