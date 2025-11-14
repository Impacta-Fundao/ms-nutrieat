from flask import Blueprint
from src.Application.Controller.client_controller import ClientController

client_bp = Blueprint("cliente", __name__)

@client_bp.route('/cliente')
def list_client():
    return ClientController.get_client()

@client_bp.route('/cliente/<int:id>')
def get_id_client(id):
    return ClientController.get_client_id(id)

@client_bp.route('/cliente', methods=['POST'])
def create_client():
    return ClientController.post_client()

@client_bp.route('/cliente/<int:id>', methods=['DELETE'])
def delete_client(id):
    return ClientController.delete_client(id)

@client_bp.route('/cliente/<int:id>', methods=['PUT'])
def update_client(id):
    return ClientController.put_client(id)

@client_bp.route('/cliente/<int:id>', methods=['PATCH'])
def update_patch_client(id):
    return ClientController.patch_client(id)
