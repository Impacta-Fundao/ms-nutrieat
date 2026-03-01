from flask import Blueprint
from src.Application.Controller.vendas_controller import VendasController

venda_bp = Blueprint('vendas', __name__)

@venda_bp.route('/vendas', methods=['GET'])
def get_vendas_all():
    return VendasController.get_vendas_all()

@venda_bp.route('/overview/vendas/<int:year>', methods=['GET'])
def get_vendas_year(year):
    return VendasController.get_vendas_year(year)