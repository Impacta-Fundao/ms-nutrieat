from flask import jsonify, request
from src.Application.Service.client_service import ClientService, ClientException

class ClientController:

    @staticmethod
    def post_client():
        try:
            request_data = request.get_json()
            service_data = ClientService.create_cliente(request_data)
            return jsonify(data=service_data, message="Cliente cadastrado com sucesso"), 200
        except ClientException as e:
            return jsonify(message=f"Erro ao cadastrar cliente: {str(e)}"), 400
        except Exception as e:
            return jsonify(message=f"Erro interno do servidor: {str(e)}"), 500
        
    @staticmethod
    def get_client():
        try:
            service_data = ClientService.listar_clientes()
            return jsonify(data=service_data), 200
        except ClientException as e:
            return jsonify(message=f"Erro ao pesquisar clientes: {str(e)}"), 400
        except Exception as e:
            return jsonify(message=f"Erro interno do servidor: {str(e)}"), 500
        
    @staticmethod
    def get_client_id(client_id):
        try:
            service_data = ClientService.get_id(client_id)
            return jsonify(data=service_data), 200
        except ClientException as e:
            return jsonify(message=f"Erro ao pesquisar cliente: {str(e)}"), 400
        except Exception as e:
            return jsonify(message=f"Erro interno do servidor: {str(e)}"), 500
        
    @staticmethod
    def delete_client(client_id):
        try:
            ClientService.deletar_cliente(client_id)
            return jsonify(message="Cliente removido com sucesso"), 200
        except ClientException as e:
            return jsonify(message=f"Erro ao deletar cliente: {str(e)}"), 400
        except Exception as e:
            return jsonify(message=f"Erro interno do servidor: {str(e)}"), 500
        
    @staticmethod
    def put_client(client_id):
        try:
            request_data = request.get_json()
            service_data = ClientService.atualizar_cliente(client_id, request_data)
            return jsonify(data=service_data, message="Cliente atualizado com sucesso"), 200
        except ClientException as e:
            return jsonify(message=f"Erro ao atualizar cliente: {str(e)}"), 400
        except Exception as e:
            return jsonify(message=f"Erro interno do servidor: {str(e)}"), 500

    @staticmethod
    def patch_client(client_id):
        try:
            request_data = request.get_json()
            service_data = ClientService.atualizar_patch_cliente(client_id, request_data)
            return jsonify(data=service_data, message="Cliente atualizado com sucesso"), 200
        except ClientException as e:
            return jsonify(message=f"Erro ao atualizar cliente: {str(e)}"), 400
        except Exception as e:
            return jsonify(message=f"Erro interno do servidor: {str(e)}"), 500
