from flask import request, jsonify, make_response
from src.Application.Service.produto_service import ProdutoService, ProdutoException

class ProdutoController:
    @staticmethod
    def post_produto():
        try:
            data = request.get_json()
            requiredField = []
            
            nome=data['nome'] if data.get('nome') else None
            preco=data.get('preco') if data.get('preco') else None
            
            requiredField.append({"nome": nome, "preco":preco})
            for field in requiredField:
                for k,v in field.items():
                    if v is None:
                        return make_response(jsonify({"message": f"Passe um valor para o campo {k}"}), 400)
                    
            produto = ProdutoService.create_produto(nome,preco).to_dict()
            return make_response(jsonify({ 
                "data": produto,
                "message": "Criado com sucesso"
                    }), 200)
        except ProdutoException as e:
            return jsonify({"message": f"Erro na requisição {e.msg}"}, 500)
        
    @staticmethod
    def get_produtos():
        try:
            data = ProdutoService.listar_produtos()
            return make_response(jsonify({"data": data}), 200)
            
        
        except ProdutoException as e:
            return make_response(jsonify({"message": f"Erro ao listar mercados: {str(e.msg)}"}), 500)
        
    @staticmethod
    def get_produto_id(produto_id):
        try:
            data = ProdutoService.get_id(produto_id)
            if not data:
                return make_response(jsonify({"message": "Não existe esse mercado cadastrado"}),400 )
            return make_response(jsonify({"data": data}), 200)
            
        except ProdutoException as e:
            return make_response(jsonify({"message": f"Erro ao buscar mercado: {str(e.msg)} | {e}"}), 500)
    
    @staticmethod
    def delete_produto(produto_id):
        try:
            data = ProdutoService.deletar_produto(produto_id)
            if not data:
                return make_response(jsonify({"message": "Não existe esse mercado cadastrado"}),400 )
            return make_response(jsonify({"data": data}), 200)
            
        except ProdutoException as e:
            return make_response(jsonify({"message": f"Erro ao deletar mercado: {str(e.msg)} | {e}"}), 500)
        
    @staticmethod
    def put_produto(produto_id):
        try:
            resp = request.get_json()
            
            if not resp:
                return make_response(jsonify({"error": "Nenhum dado fornecido"}), 400)
            
            updateProduto = ProdutoService.atualizar_produto(produto_id,resp)
            
            return make_response(jsonify({"data": updateProduto, "message": "Atualizado com sucesso"}), 200)
            
        except ProdutoException as e:
            return make_response(jsonify({"message": f"{e.msg} | {e}"}),400 )
    
    
    @staticmethod
    def patch_produto(produto_id):
        try:
            resp = request.get_json()
            
            if not resp:
                return make_response(jsonify({"error": "Nenhum dado fornecido"}), 400)
            
            updateProduto = ProdutoService.atualizar_patch_produto(produto_id,resp)
            
            return make_response(jsonify({"data": updateProduto, "message": "Atualizado com sucesso"}))
            
        except ProdutoException as e:
            return make_response(jsonify({"message": f"{e.msg} | {e}"}),400 )
