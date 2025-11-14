from flask import Blueprint
from src.Application.Controller.product_controller import ProductController

product_bp = Blueprint('product', __name__)

@product_bp.route('/produto', methods=['GET'])
def list_product():
    return ProductController.get_product()

@product_bp.route('/produto/<int:id>', methods=['GET'])
def get_id_product(id):
    return ProductController.get_product_id(id)

@product_bp.route('/produto', methods=['POST'])
def create_product():
    return ProductController.post_product()

@product_bp.route('/produto/<int:id>', methods=['DELETE'])
def delete_product(id):
    return ProductController.delete_product(id)

@product_bp.route('/produto/<int:id>', methods=['PUT'])
def update_product(id):
    return ProductController.put_product(id)

@product_bp.route('/produto/<int:id>', methods=['PATCH'])
def update_patch_product(id):
    return ProductController.patch_product(id)
