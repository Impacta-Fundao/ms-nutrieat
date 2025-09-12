from flask import Blueprint, jsonify, make_response
from src.Application.Controller.produto_controller import ProdutoController

produto_bp = Blueprint('produto', __name__) 

def init_routeClients(app):
    app.register_blueprint(produto_bp)
    @app.route('/', methods=["GET"])
    def raiz():
        return make_response(jsonify({
            "message": "API - OK"
        }), 200)

@produto_bp.route('/produto', methods=['GET'])
def list_product():
    return ProdutoController.get_produtos()

@produto_bp.route('/produto/<int:id>', methods=['GET'])
def get_id_product(id):
    return ProdutoController.get_produto_id(id)

@produto_bp.route('/produto', methods=['POST'])
def create_product():
    return ProdutoController.post_produto()

@produto_bp.route('/produto/<int:id>', methods=['DELETE'])
def delete_product(id):
    return ProdutoController.delete_produto(id)

@produto_bp.route('/produto/<int:id>', methods=['PUT'])
def update_product(id):
    return ProdutoController.put_produto(id)

@produto_bp.route('/produto/<int:id>', methods=['PATCH'])
def update_patch_product(id):
    return ProdutoController.patch_produto(id)
    
