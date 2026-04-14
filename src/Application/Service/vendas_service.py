from src.Infrastructure.models.vendas import Vendas
from src.Infrastructure.models.itens_vendas import ItensVendas
from src.Infrastructure.models.produto import Produto
from src import db
from src.utils.return_service import ReturnVendas
from sqlalchemy import func, extract, desc
from datetime import datetime


class VendasException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg


class VendasService:

    @staticmethod
    def get_vendas_all():
        vendas = Vendas.query.all()
        if not vendas:
            raise VendasException("Não foram encontrados vendas cadastrados")
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

    @staticmethod
    def get_produtos_year(year):
        data_inicio = datetime(year, 1, 1)
        data_fim = datetime(year + 1, 1, 1)

        mes_ano = func.to_char(Vendas.data_venda, 'YYYY-MM')
        mes_numero = func.to_char(Vendas.data_venda, 'MM')
        mes_nome = func.to_char(Vendas.data_venda, 'Month')

        vendas_mensais = db.session.query(
            mes_ano.label("mes_ano"),
            mes_numero.label("mes_numero"),
            mes_nome.label("mes_nome"),
            ItensVendas.produto_id.label("produto_id"),
            Produto.nome.label("nome_produto"),
            func.sum(ItensVendas.quantidade).label("total_vendido")
        ).join(
            Vendas, ItensVendas.venda_id == Vendas.id
        ).join(
            Produto, ItensVendas.produto_id == Produto.id
        ).filter(
            Vendas.data_venda >= data_inicio,
            Vendas.data_venda < data_fim
        ).group_by(
            mes_ano,
            mes_numero,
            mes_nome,
            ItensVendas.produto_id,
            Produto.nome
        ).subquery()

        ranking = db.session.query(
            vendas_mensais.c.mes_ano,
            vendas_mensais.c.mes_numero,
            vendas_mensais.c.mes_nome,
            vendas_mensais.c.produto_id,
            vendas_mensais.c.nome_produto,
            vendas_mensais.c.total_vendido,
            func.row_number().over(
                partition_by=vendas_mensais.c.mes_ano,
                order_by=desc(vendas_mensais.c.total_vendido)
            ).label("posicao")
        ).subquery()

        resultados = db.session.query(
            ranking.c.mes_ano,
            ranking.c.mes_numero,
            ranking.c.mes_nome,
            ranking.c.produto_id,
            ranking.c.nome_produto,
            ranking.c.total_vendido
        ).filter(
            ranking.c.posicao == 1
        ).order_by(
            ranking.c.mes_ano
        ).all()

        if not resultados:
            raise VendasException(f"Não foram encontrados produtos para o ano de {year}")

        dados = [
            {
                "mes_numero": r.mes_numero.strip(),
                "mes_nome": r.mes_nome.strip(),
                "produto_id": r.produto_id,
                "nome_produto": r.nome_produto,
                "total_vendido": int(r.total_vendido)
            }
            for r in resultados
        ]

        return {
            "ano": year,
            "meses": dados
        }
