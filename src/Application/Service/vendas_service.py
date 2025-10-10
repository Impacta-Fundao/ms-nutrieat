from src.Domain.vendas import VendaDomain, ItemVendaDomain, StatusPagamento, FormaPagamento
from src.Infrastructure.models.vendas import  Vendas
from src import db
from decimal import Decimal

class VendasException(Exception):
    def __init__(self, *args):
        super().__init__(*args)
        self.args = args

class VendasService:
    
    @staticmethod
    def create_venda(cliente_id, itens_venda, status_pagamento, forma_pagamento, valor_total=None):
        try:
            status_pagamento = StatusPagamento(status_pagamento)
            forma_pagamento = FormaPagamento(forma_pagamento)
            
            itens_venda = []
            for item_data in itens_venda:
                item = ItemVendaDomain(
                    produto_id=item_data['produto_id'],
                    quantidade=item_data['quantidade'],
                    preco_unitario=Decimal(str(item_data['preco_unitario']))
                )
                itens_venda.append(item)
                
            new_venda = VendaDomain(cliente_id, itens_venda, status_pagamento, forma_pagamento,valor_total)
            venda = Vendas(
            cliente_id=new_venda.cliente_id,
            data_venda=new_venda.data_venda,
            valor_total=new_venda.valor_total,
            status_pagamento=new_venda.status_pagamento.value,
            forma_pagamento=new_venda.forma_pagamento.value,
            )
            db.session.add(venda)
            db.session.commit()
            return venda
        except ValueError as e:
            raise VendasException(F"Erro de converção: {str(e)}")
        except Exception as e:
            raise VendasException(f"Erro ao criar venda: {str(e)}")
        
    @staticmethod
    def listar_vendas():
        try:
            data = Vendas.query.all()
            vendas_json = []
            
            for venda in data:
                venda_dict = {
                    'id': venda.id,
                    'cliente_id': venda.cliente_id,
                    'data_venda': venda.data_venda.isoformat() if venda.data_venda else None,
                    'valor_total': float(venda.valor_total) if venda.valor_total else 0.0,
                    'status_pagamento': venda.status_pagamento.value if venda.status_pagamento else None,
                    'created_at': venda.created_at.isoformat() if venda.created_at else None,
                    'updated_at': venda.updated_at.isoformat() if venda.updated_at else None,
                    'forma_pagamento': venda.forma_pagamento.value if venda.forma_pagamento else None,
                }
                
                if hasattr(venda, 'cliente') and venda.cliente:
                    venda_dict['cliente'] = {
                        'id': venda.cliente.id,
                        'nome': venda.cliente.nome
                    }
                
                vendas_json.append(venda_dict)
                
            return vendas_json
            
        except Exception as e:
            raise VendasException(f"Erro ao listar vendas: {str(e)}")