from flask import jsonify, request, make_response
from src.Application.Service.vendas_service import VendasService, VendasException

class VendaController:
    @staticmethod
    def post_venda():
        try:
            data = request.get_json()
            venda = VendasService.create_venda(
                data.get("cliente_id"), 
                data.get("itens_venda"),
                data.get("status_pagamento"),
                data.get("forma_pagamento"),
                data.get("data_venda"),
                data.get("valor_total"),
                data.get("created_at"),
                data.get("updated_at")).to_dict()    
            return make_response(jsonify({
                "data": venda,
                "message": "Criado com sucesso"
            }),200)
        except VendasException as e:
            return jsonify({"message": f'Erro na requisição {e.args}'}, 500)
        
    @staticmethod
    def get_vendas():
        try:
            data = VendasService.listar_vendas()
            return make_response(jsonify({"data": data}), 200)
        except VendasException as e:
            return make_response(jsonify({"message" : f'Erro ao listar vendas {e.args}'}))