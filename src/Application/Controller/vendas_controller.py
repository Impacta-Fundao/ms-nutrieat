from flask import request, jsonify
from src.Application.Service.vendas_service import VendasService, VendasException

class VendasController:
    
    @staticmethod
    def get_vendas_all():
        try:
            requets_data = VendasService.get_vendas_all()
            return jsonify(data=requets_data), 200
        except VendasException as e:
            return jsonify(message=f"Erro ao pesquisar vendas: {str(e)}"), 400
        except Exception as e:
            return jsonify(message=f"Erro interno do servidor: {str(e)}"), 500
    
    @staticmethod
    def get_vendas_year(year):
        try:
            service_data = VendasService.get_vendas_year(year)
            return jsonify(data=service_data), 200
        except VendasException as e:
            return jsonify(message=f"Erro ao pesquisar vendas: {str(e)}"), 400
        except Exception as e:
            return jsonify(message=f"Erro interno do servidor: {str(e)}"), 500