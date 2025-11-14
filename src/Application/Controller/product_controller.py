from flask import request, jsonify
from src.Application.Service.product_service import ProductService, ProductException

class ProductController:
    
    @staticmethod
    def post_product():
        try:
            request_data = request.get_json()
            service_data = ProductService.cadastrar_produto(request_data)
            return jsonify(data=service_data, message="Produto criado com sucesso"), 200
        except ProductException as e:
            return jsonify(message=f"Erro ao cadastrar produto: {str(e)}"), 400
        except Exception as e:
            return jsonify(message=f"Erro interno do servidor: {str(e)}"), 500
        
    @staticmethod
    def get_product():
        try:
            service_data = ProductService.listar_produtos()
            return jsonify(data=service_data), 200
        except ProductException as e:
            return jsonify(message=f"Erro ao pesquisar produtos: {str(e)}"), 400
        except Exception as e:
            return jsonify(message=f"Erro interno do servidor: {str(e)}"), 500
        
    @staticmethod
    def get_product_id(product_id):
        try:
            service_data = ProductService.listar_produto_id(product_id)
            return jsonify(data=service_data), 200
        except ProductException as e:
            return jsonify(message=f"Erro ao pesquisar produto: {str(e)}"), 400
        except Exception as e:
            return jsonify(message=f"Erro interno do servidor: {str(e)}"), 500
    
    @staticmethod
    def delete_product(product_id):
        try:
            ProductService.deletar_produto(product_id)
            return jsonify(message="Produto removido com sucesso"), 200
        except ProductException as e:
            return jsonify(message=f"Erro ao deletar produto: {str(e)}"), 400
        except Exception as e:
            return jsonify(message=f"Erro interno do servidor: {str(e)}"), 500
    
    @staticmethod
    def put_product(product_id):
        try:
            request_data = request.get_json()
            service_data = ProductService.atualizar_produto(product_id, request_data)
            return jsonify(data=service_data, message="Produto atualizado com sucesso"), 200
        except ProductException as e:
            return jsonify(message=f"Erro ao atualizar produto: {str(e)}"), 400
        except Exception as e:
            return jsonify(message=f"Erro interno do servidor: {str(e)}"), 500
    
    @staticmethod
    def patch_product(product_id):
        try:
            request_data = request.get_json()
            service_data = ProductService.atualizar_patch_produto(product_id, request_data)
            return jsonify(data=service_data, message="Produto atualizado com sucesso"), 200
        except ProductException as e:
            return jsonify(message=f"Erro ao atualizar produto: {str(e)}"), 400
        except Exception as e:
            return jsonify(message=f"Erro interno do servidor: {str(e)}"), 500
