from src.Infrastructure.models.vendas import Vendas
from src import db
from src.utils.return_service import ReturnVendas
from sqlalchemy import func, extract

class VendasException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg
        

class VendasService:
    
    @staticmethod
    def get_vendas_all():
        vendas = Vendas.query.all()
        if not vendas: raise VendasException("Não foram encontrados vendas cadastrados")
        return [ReturnVendas.vendas(v) for v in vendas]
    
    @staticmethod
    def get_vendas_year(year):
    
        ano = func.to_char(Vendas.data_venda, 'YYYY')
        mes_numero = func.to_char(Vendas.data_venda, 'MM')
        mes_nome = func.to_char(Vendas.data_venda, 'Month')
        
        
        query = db.session.query(
            ano.label('ano'),
            mes_numero.label('mes_numero'),
            mes_nome.label('mes_nome'),
            func.count().label('quantidade_vendas')
        ).filter(
            extract('year', Vendas.data_venda) == year
        ).group_by(
            ano,
            mes_numero,
            mes_nome
        ).order_by(
            'ano', 'mes_numero'
        )
        
   
        resultados = query.all()
        
        if not resultados:
            raise VendasException(f"Não foram encontradas vendas para o ano de {year}")
            
        dados_meses = [
            {
                "mes_numero": r.mes_numero.strip(),
                "mes_nome": r.mes_nome.strip(),
                "quantidade_vendas": r.quantidade_vendas
            } for r in resultados
        ]

        return {
            "ano": year,
            "meses": dados_meses
        }
