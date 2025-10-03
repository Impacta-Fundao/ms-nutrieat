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
    def create_cliente(nome,cpf,data_nascimento,numero,turno, sala, email):
        new_cliente = ClientDomain(nome,cpf,data_nascimento,numero,turno,sala,email)
        cliente = Cliente(nome=new_cliente.nome,cpf=new_cliente.cpf,data_nascimento=str(new_cliente.data_nascimento), numero=new_cliente.numero, sala=new_cliente.sala, turno=new_cliente.turno, email=new_cliente.email)
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
            'idade': calcularIdade(cliente.data_nascimento),
            'numero' : cliente.numero,
            'sala' : cliente.sala,
            'turno' : cliente.turno,
            'email' : cliente.email
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
            'idade': calcularIdade(data.data_nascimento),
            'numero' : data.numero,
            'sala' : data.sala,
            'turno' : data.turno,
            'email' : data.email
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
            'data_nascimento': cliente_data.get('data_nascimento'),
            'numero' : cliente_data.get('numero'),
            'sala': cliente_data.get('sala'),
            'turno': cliente_data.get('turno'),
            'email' : cliente_data.get('email')
        }
        
        for field, value in required_fields.items():
            if value is None:
                raise ClienteException(f"O campo '{field}' é obrigatório.")
        
        data.nome = required_fields['nome']
        data.cpf = required_fields['cpf']
        data.data_nascimento = required_fields['data_nascimento']
        data.numero = required_fields['numero']
        data.sala = required_fields['sala']
        data.turno = required_fields['turno']
        data.email = required_fields['email']
        
        db.session.commit()
        
        return {
            'id': data.id,
            'nome': data.nome,
            'cpf': data.cpf,
            'idade': calcularIdade(data.data_nascimento),
            'numero' : data.numero,
            'sala' : data.sala,
            'turno' : data.turno,
            'email' : data.email
        }
    
    @staticmethod
    def atualizar_patch_cliente(cliente_id, cliente_data):
        data = Cliente.query.get(cliente_id)
        if data is None:
            raise ClienteException("Cliente não encontrado")
        
        if 'nome' in cliente_data:
            data.nome = cliente_data['nome']
        if 'cpf' in cliente_data:
            data.cpf = cliente_data['cpf']
        if 'data_nascimento' in cliente_data:
            data.data_nascimento = cliente_data['data_nascimento']
        if 'numero' in cliente_data:
            data.numero = cliente_data['numero']
        if 'sala' in cliente_data:
            data.sala = cliente_data['sala']
        if 'turno' in cliente_data:
            data.turno = cliente_data['turno']
        if 'email' in cliente_data:
            data.email = cliente_data['email']
        
        
        db.session.commit()
        
        return {
            'id': data.id,
            'nome': data.nome,
            'cpf': data.cpf,
            'idade': calcularIdade(data.data_nascimento),
            'numero' : data.numero,
            'sala' : data.sala,
            'turno' : data.turno,
            'email' : data.email
        }