from flask import jsonify, request
from src.Application.Service.admin_service import AdminService, AdminException, LoginException

class AdminController:

    @staticmethod
    def post_admin():
        try:
            request_data = request.get_json()
            service_data = AdminService.criar_admin(request_data)
            return jsonify(data=service_data, message="Admin cadastrado com sucesso"), 200
        except AdminException as e:
            return jsonify(message=f"Erro ao cadastrar admin: {str(e)}"), 400
        except Exception as e:
            return jsonify(message=f"Erro interno do servidor: {str(e)}"), 500
        
    @staticmethod
    def get_admin():
        try:
            service_data = AdminService.listar_admins()
            return jsonify(data=service_data), 200
        except AdminException as e:
            return jsonify(message=f"Erro ao pesquisar admins: {str(e)}"), 400
        except Exception as e:
            return jsonify(message=f"Erro interno do servidor: {str(e)}"), 500
        
    @staticmethod
    def get_admin_id(adm_id):
        try:
            service_data = AdminService.get_id(adm_id)
            return jsonify(data=service_data), 200
        except AdminException as e:
            return jsonify(message=f"Erro ao pesquisar admin: {str(e)}"), 400
        except Exception as e:
            return jsonify(message=f"Erro interno do servidor: {str(e)}"), 500
        
    @staticmethod
    def delete_admin(adm_id):
        try:
            AdminService.deletar_admin(adm_id)
            return jsonify(message="Admin removido com sucesso"), 200
        except AdminException as e:
            return jsonify(message=f"Erro ao deletar admin: {str(e)}"), 400
        except Exception as e:
            return jsonify(message=f"Erro interno do servidor: {str(e)}"), 500
        
    @staticmethod
    def put_admin(adm_id):
        try:
            request_data = request.get_json()
            service_data = AdminService.atualizar_admin(adm_id, request_data)
            return jsonify(data=service_data, message="Admin atualizado com sucesso"), 200
        except AdminException as e:
            return jsonify(message=f"Erro ao atualizar admin: {str(e)}"), 400
        except Exception as e:
            return jsonify(message=f"Erro interno do servidor: {str(e)}"), 500

    @staticmethod
    def patch_admin(adm_id):
        try:
            request_data = request.get_json()
            service_data = AdminService.atualizar_patch_admin(adm_id, request_data)
            return jsonify(data=service_data, message="Admin atualizado com sucesso"), 200
        except AdminException as e:
            return jsonify(message=f"Erro ao atualizar admin: {str(e)}"), 400
        except Exception as e:
            return jsonify(message=f"Erro interno do servidor: {str(e)}"), 500

    @staticmethod
    def login_admin():
        try:
            request_data = request.get_json()
            service_data = AdminService.login_admin(request_data)
            return jsonify(data=service_data, message="Logado com sucesso"), 200
        except LoginException as e:
            return jsonify(message=f"Erro na tentativa de login: {str(e)}"), 400
        except Exception as e:
            return jsonify(message=f"Erro interno do servidor: {str(e)}"), 500
