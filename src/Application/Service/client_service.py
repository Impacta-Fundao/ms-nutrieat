from src.Infrastructure.models.cliente import Cliente
from src.utils.return_service import ReturnClients
from src import db

class ClientException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

class ClientService:

    @staticmethod
    def create_cliente(cliente_data):
        if not cliente_data: raise ClientException("Nenhum dado fornecido")
        
        data_itens = {
            "nome": cliente_data.get("nome"), 
            "cpf": cliente_data.get("cpf"), 
            "data_nascimento": cliente_data.get("data_nascimento"), 
            "numero": cliente_data.get("numero"), 
            "sala": cliente_data.get("sala"), 
            "turno": cliente_data.get("turno"), 
            "email": cliente_data.get("email")
            }

        for k, v in data_itens.items():
            if not v: raise ClientException(f"Passe um valor para o campo '{k}'")
        
        if int(data_itens["data_nascimento"].split("-")[1]) > 12: raise ClientException("Data inválida")
        if len(data_itens["data_nascimento"].split("-")[0]) != 4: raise ClientException("Formato de data errado. Passe no formato YYYY-MM-DD")
        if int(data_itens["data_nascimento"].split("-")[2]) > 31: raise ClientException("Data inválida")

        cliente = Cliente(nome=data_itens["nome"], cpf=data_itens["cpf"], data_nascimento=str(data_itens["data_nascimento"]), 
                          numero=data_itens["numero"], sala=data_itens["sala"], turno=data_itens["turno"], email=data_itens["email"])
        
        db.session.add(cliente)
        db.session.commit()

        novo_cliente = Cliente.query.order_by(Cliente.id.desc()).first()

        return ReturnClients.clients(novo_cliente)
    
    @staticmethod
    def listar_clientes():
        clientes = Cliente.query.all()

        if not clientes: raise ClientException("Não foram encontrados clientes cadastrados")
        
        return [ReturnClients.clients(cliente) for cliente in clientes]

    
    @staticmethod
    def get_id(cliente_id):
        cliente = Cliente.query.get(cliente_id)

        if not cliente: raise ClientException("Cliente não encontrado")
        
        return ReturnClients.clients(cliente)
    
    @staticmethod
    def deletar_cliente(cliente_id):
        cliente = Cliente.query.get(cliente_id)

        if not cliente: raise ClientException("Cliente não encontrado")
        
        db.session.delete(cliente)
        db.session.commit()

    @staticmethod
    def atualizar_cliente(cliente_id, cliente_data):
        if not cliente_data: raise ClientException("Nenhum dado fornecido")

        cliente = Cliente.query.get(cliente_id)
        
        if not cliente: raise ClientException("Cliente não encontrado")
        
        data_itens = {
            "nome": cliente_data.get("nome"),
            "cpf": cliente_data.get("cpf"),
            "data_nascimento": cliente_data.get("data_nascimento"),
            "numero" : cliente_data.get("numero"),
            "sala": cliente_data.get("sala"),
            "turno": cliente_data.get("turno"),
            "email" : cliente_data.get("email")
        }
        
        for k, v in data_itens.items():
            if not v: raise ClientException(f"O campo '{k}' é obrigatório")
        
        cliente.nome = data_itens["nome"]
        cliente.cpf = data_itens["cpf"]
        cliente.data_nascimento = data_itens["data_nascimento"]
        cliente.numero = data_itens["numero"]
        cliente.sala = data_itens["sala"]
        cliente.turno = data_itens["turno"]
        cliente.email = data_itens["email"]
        
        db.session.commit()
        
        return ReturnClients.clients(cliente)
    
    @staticmethod
    def atualizar_patch_cliente(cliente_id, cliente_data):
        if not cliente_data: raise ClientException("Nenhum dado fornecido")

        cliente = Cliente.query.get(cliente_id)
        
        if not cliente: raise ClientException("Cliente não encontrado")
        
        if cliente_data.get("nome"): cliente.nome = cliente_data["nome"]
        if cliente_data.get("cpf"): cliente.cpf = cliente_data["cpf"]
        if cliente_data.get("data_nascimento"): cliente.data_nascimento = cliente_data["data_nascimento"]
        if cliente_data.get("numero"): cliente.numero = cliente_data["numero"]
        if cliente_data.get("sala"): cliente.sala = cliente_data["sala"]
        if cliente_data.get("turno"): cliente.turno = cliente_data["turno"]
        if cliente_data.get("email"): cliente.email = cliente_data["email"]
        
        db.session.commit()
        
        return ReturnClients.clients(cliente)
