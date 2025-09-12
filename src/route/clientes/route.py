from flask import Blueprint, jsonify, make_response
from src.Application.Controller.client_controller import ClienteController

client_bp = Blueprint("cliente", __name__)

def init_routeProduct(app):
    app.register_blueprint(client_bp)

@client_bp.route('/cliente')
def list_client():
    return ClienteController.get_clientes()

@client_bp.route('/cliente/<int:id>')
def get_id_client(id):
    return ClienteController.get_cliente_id(id)

@client_bp.route('/cliente', methods=['POST'])
def create_client():
    return ClienteController.post_cliente()


@client_bp.route('/cliente/<int:id>', methods=['DELETE'])
def delete_client(id):
    return ClienteController.delete_cliente(id)

@client_bp.route('/cliente/<int:id>', methods=['PUT'])
def update_client(id):
    return ClienteController.put_cliente(id)

@client_bp.route('/cliente/<int:id>', methods=['PATCH'])
def update_patch_client(id):
    return ClienteController.patch_cliente(id)
