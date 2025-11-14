from datetime import date, datetime

class ReturnClients():

    @staticmethod
    def _calcular_idade(data_nascimento):

        if isinstance(data_nascimento, str):
            ano, mes, dia = map(int, data_nascimento.split("-"))
            data_nascimento = date(ano, mes, dia)

        if isinstance(data_nascimento, datetime):
            data_nascimento = data_nascimento.date()

        hoje = date.today()
        idade = hoje.year - data_nascimento.year

        if (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day):
            idade -= 1

        return idade

    @staticmethod
    def clients(client):
        return {
            "id": client.id,
            "nome": client.nome,
            "cpf": client.cpf,
            "idade": ReturnClients._calcular_idade(client.data_nascimento),
            "numero": client.numero,
            "sala": client.sala,
            "turno": client.turno,
            "email": client.email
        } 

class ReturnProducts():

    @staticmethod
    def products(product):
        return {
            "id": product.id, 
            "nome": product.nome, 
            "preco": product.preco
        }
    
class ReturnAdmin():

    @staticmethod
    def admins(adm):
        return {
            "id": adm.id,
            "nome": adm.nome,
            "cpf": adm.cpf,
            "email": adm.email,
            "celular": adm.celular
        } 
