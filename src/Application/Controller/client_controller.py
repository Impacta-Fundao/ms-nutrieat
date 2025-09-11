from flask import jsonify, request, make_response
from src.Application.Service.cliente_service import ClienteService,  ClienteException

class ClienteController:
    @staticmethod
    def post_cliente():
        try:
            data = request.get_json()
            requiredField = []
            
            nome=data['nome'] if data.get('nome') else None
            cpf=data.get('cpf') if data.get('cpf') else None
            data_nascimento=data.get('data_nascimento') if (data.get('data_nascimento')) else None
            if int(data_nascimento.split('-')[1]) > 12:
                return make_response({"message" :"Data inválida"},400)
            if len(data_nascimento.split('-')[0]) != 4:
                return make_response({'message':"Formato de data errado. Passe no formato YYYY-MM-DD"}, 400)
            if int(data_nascimento.split('-')[2]) > 30:
                return make_response("Data inválida",400)
            
            requiredField.append({"nome": nome, "cpf":cpf, "data_nascimento":data_nascimento})
            for field in requiredField:
                for k,v in field.items():
                    if v is None:
                        return make_response(jsonify({"message": f"Passe um valor para o campo {k}"}), 400)
                    
            cliente = ClienteService.create_cliente(nome,cpf,data_nascimento).to_dict()
            return make_response(jsonify({ 
                "data": cliente,
                "message": "Criado com sucesso"
                    }), 200)
        except ClienteException as e:
            return jsonify({"message": f"Erro na requisição {e.msg}"}, 500)
        
    @staticmethod
    def get_clientes():
        try:
            data = ClienteService.listar_clientes()
            return make_response(jsonify({"data": data}), 200)
            
        
        except ClienteException as e:
            return make_response(jsonify({"message": f"Erro ao listar clientes: {str(e.msg)}"}), 500)
        
    
    @staticmethod
    def get_cliente_id(cliente_id):
        try:
            data = ClienteService.get_id(cliente_id)
            if not data:
                return make_response(jsonify({"message": "Não existe esse cliente cadastrado"}),400 )
            return make_response(jsonify({"data": data}), 200)
            
        except ClienteException as e:
            return make_response(jsonify({"message": f"Erro ao buscar cliente: {str(e.msg)} | {e}"}), 500)
        
    @staticmethod
    def delete_cliente(cliente_id):
        try:
            data = ClienteService.deletar_cliente(cliente_id)
            if not data:
                return make_response(jsonify({"message": "Não existe esse cliente cadastrado"}),400 )
            return make_response(jsonify({"data": data}), 200)
            
        except ClienteException as e:
            return make_response(jsonify({"message": f"Erro ao deletar cliente: {str(e.msg)} | {e}"}), 500)
        
    @staticmethod
    def put_cliente(cliente_id):
        try:
            data = request.get_json()
            
            if not data:
                return make_response(jsonify({"message": "Nenhum dado fornecido para atualização"}), 400)

            cliente = ClienteService.atualizar_cliente(cliente_id, data)
            return make_response(jsonify({ 
                "data": cliente,
                "message": "Atualizado com sucesso"
                    }), 200)
        except ClienteException as e:
            return jsonify({"message": f"Erro na requisição {e.msg}"}, 500)
        

    @staticmethod
    def patch_cliente(cliente_id):
        try:
            data = request.get_json()
            
            if not data:
                return make_response(jsonify({"message": "Nenhum dado fornecido para atualização"}), 400)

            cliente = ClienteService.atualizar_cliente(cliente_id, data)
            return make_response(jsonify({ 
                "data": cliente,
                "message": "Atualizado com sucesso"
                    }), 200)
        except ClienteException as e:
            return jsonify({"message": f"Erro na requisição {e.msg}"}, 500)