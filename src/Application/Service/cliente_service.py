from src.Domain.cliente import ClientDomain
from src.Infrastructure.models.clientes import Cliente
from src.utils.calcularIdade import calcularIdade
from src import db

class ClienteException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

class ClienteService:
    
    @staticmethod
    def create_cliente(nome,cpf,data_nascimento):
        new_cliente = ClientDomain(nome,cpf,data_nascimento)
        cliente = Cliente(nome=new_cliente.nome,cpf=new_cliente.cpf,data_nascimento=new_cliente.data_nascimento)
        db.session.add(cliente)
        db.session.commit()
        return cliente
    
    @staticmethod
    def listar_clientes():
        data = Cliente.query.all()
        cliente_json = [{
            'id': cliente.id,
            'nome': cliente.nome,
            'cpf': cliente.cpf,
            'data_nascimento': cliente.data_nascimento,
            'idade': calcularIdade(cliente.data_nascimento)
        } for cliente in data]
        
        return cliente_json
    
    @staticmethod
    def get_id(cliente_id):
        data = Cliente.query.get(cliente_id)

        if data is None: raise ClienteException("Esse cliente não está cadastrado")
        cliente_json = {
            'id': data.id,
            'nome': data.nome,
            'cpf': data.cpf,
            'data_nascimento': data.data_nascimento,
            'idade': calcularIdade(data.data_nascimento)
        } 
        
        return cliente_json
    
    @staticmethod
    def deletar_cliente(cliente_id):
        data = Cliente.query.get(cliente_id)
        if data is None:return None
        
        db.session.delete(data)
        db.session.commit()
        return {"message": "Cliente deletado com sucesso"}
    

    @staticmethod
    def atualizar_cliente(cliente_id, cliente_data):
        data = Cliente.query.get(cliente_id)
        if data is None:
            raise ClienteException("Cliente não encontrado")
        
        required_fields = {
            'nome': cliente_data.get('nome'),
            'cpf': cliente_data.get('cpf'),
            'data_nascimento': cliente_data.get('data_nascimento')
        }
        
        for field, value in required_fields.items():
            if value is None:
                raise ClienteException(f"O campo '{field}' é obrigatório.")
        
        data.nome = required_fields['nome']
        data.cpf = required_fields['cpf']
        data.data_nascimento = required_fields['data_nascimento']
        
        db.session.commit()
        
        return {
            'id': data.id,
            'nome': data.nome,
            'cpf': data.cpf,
            'data_nascimento': data.data_nascimento,
            'idade': calcularIdade(data.data_nascimento)
        }