from flask import Blueprint
from src.Application.Controller.admin_controller import AdminController

login_admin_bp = Blueprint("admin_login", __name__)

@login_admin_bp.route('/admin/login', methods=['POST'])
def login_admin():
    return AdminController.login_admin()
