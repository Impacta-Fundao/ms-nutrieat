from flask import Blueprint, jsonify, make_response
from src.Application.Controller.vendas_controller import VendaController

vendas_bp = Blueprint('vendas', __name__)

def init_routeVendas(app):
    app.register_blueprint(vendas_bp)
    
@vendas_bp.route('/vendas')
def list_sales():
    return VendaController.get_vendas()

@vendas_bp.route('/vendas', methods=["POST"])
def create_sale():
    return VendaController.post_venda()