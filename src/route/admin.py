from flask import Blueprint
from src.Application.Controller.admin_controller import AdminController

admin_bp = Blueprint("admin", __name__)

@admin_bp.route('/admin')
def list_admin():
    return AdminController.get_admin()

@admin_bp.route('/admin/<int:id>')
def get_id_admin(id):
    return AdminController.get_admin_id(id)

@admin_bp.route('/admin', methods=['POST'])
def create_admin():
    return AdminController.post_admin()

@admin_bp.route('/admin/<int:id>', methods=['DELETE'])
def delete_admin(id):
    return AdminController.delete_admin(id)

@admin_bp.route('/admin/<int:id>', methods=['PUT'])
def update_admin(id):
    return AdminController.put_admin(id)

@admin_bp.route('/admin/<int:id>', methods=['PATCH'])
def update_patch_admin(id):
    return AdminController.patch_admin(id)
