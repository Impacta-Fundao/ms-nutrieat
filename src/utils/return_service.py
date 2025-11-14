from .calcular_idade import calcular_idade

class ReturnClients():

    @staticmethod
    def clients(client):
        return {
            "id": client.id,
            "nome": client.nome,
            "cpf": client.cpf,
            "idade": calcular_idade(client.data_nascimento),
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
