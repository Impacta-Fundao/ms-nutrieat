from flask import Blueprint
from src.Application.Controller.admin_controller import AdminController

login_admin_bp = Blueprint("admin_login", __name__)

@login_admin_bp.route('/admin/register', methods=['POST'])
def register_admin():
    return AdminController.register_admin()

@login_admin_bp.route('/admin/login', methods=['POST'])
def login_admin():
    return AdminController.login_admin()

@login_admin_bp.route('/admin/refresh', methods=['POST'])
def refresh_admin():
    return AdminController.refresh_admin()

@login_admin_bp.route('/admin/me', methods=['GET'])
def me_admin():
    return AdminController.me_admin()

@login_admin_bp.route('/admin/account/<int:id>', methods=['GET'])
def get_admin_account(id):
    return AdminController.get_admin_account(id)

@login_admin_bp.route('/admin/account/<int:id>', methods=['PATCH'])
def patch_admin_account(id):
    return AdminController.patch_admin_account(id)
