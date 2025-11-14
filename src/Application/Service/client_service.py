from src.Infrastructure.models.cliente import Cliente
from src.utils.return_service import ReturnClients
from datetime import datetime, date
from src import db

class ClientException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

class ClientService:

    @staticmethod
    def _parse_data_nascimento(valor):
        if isinstance(valor, date): return valor
        if isinstance(valor, str):
            try:
                return datetime.strptime(valor, "%Y-%m-%d").date()
            except ValueError:
                raise ClientException("Formato de data inválido. Use YYYY-MM-DD")
        raise ClientException("Tipo de data inválido")

    @staticmethod
    def _get_cliente_or_404(cliente_id):
        cliente = Cliente.query.get(cliente_id)
        if not cliente: raise ClientException("Cliente não encontrado")
        return cliente

    @staticmethod
    def _update_fields(cliente, dados):
        for campo, valor in dados.items():
            if valor is None: continue
            if not isinstance(valor, str): raise ClientException(f"Passe o valor do campo '{campo}' em String")
            if campo == "data_nascimento":
                valor = ClientService._parse_data_nascimento(valor)

            setattr(cliente, campo, valor)

    @staticmethod
    def criar_cliente(cliente_data):
        if not cliente_data: raise ClientException("Nenhum dado fornecido")

        for campo in ["nome", "cpf", "data_nascimento", "numero", "sala", "turno", "email"]:
            if not cliente_data.get(campo): raise ClientException(f"Passe um valor para o campo '{campo}'")
            if not isinstance(cliente_data.get(campo), str): raise ClientException(f"Passe o valor do campo '{campo}' em String")

        data_nasc = ClientService._parse_data_nascimento(cliente_data["data_nascimento"])

        cliente = Cliente(
            nome=cliente_data["nome"],
            cpf=cliente_data["cpf"],
            data_nascimento=data_nasc,
            numero=cliente_data["numero"],
            sala=cliente_data["sala"],
            turno=cliente_data["turno"],
            email=cliente_data["email"]
        )

        db.session.add(cliente)
        db.session.commit()

        return ReturnClients.clients(cliente)
    
    @staticmethod
    def listar_clientes():
        clientes = Cliente.query.all()
        if not clientes: raise ClientException("Não foram encontrados clientes cadastrados")
        return [ReturnClients.clients(c) for c in clientes]

    @staticmethod
    def get_id(cliente_id):
        cliente = ClientService._get_cliente_or_404(cliente_id)
        return ReturnClients.clients(cliente)
    
    @staticmethod
    def deletar_cliente(cliente_id):
        cliente = ClientService._get_cliente_or_404(cliente_id)
        db.session.delete(cliente)
        db.session.commit()

    @staticmethod
    def atualizar_cliente(cliente_id, cliente_data):
        if not cliente_data: raise ClientException("Nenhum dado fornecido")

        cliente = ClientService._get_cliente_or_404(cliente_id)

        for campo in ["nome", "cpf", "data_nascimento", "numero", "sala", "turno", "email"]:
            if not cliente_data.get(campo): raise ClientException(f"O campo '{campo}' é obrigatório")

        dados = cliente_data.copy()
        dados["data_nascimento"] = ClientService._parse_data_nascimento(dados["data_nascimento"])

        ClientService._update_fields(cliente, dados)
        db.session.commit()

        return ReturnClients.clients(cliente)
    
    @staticmethod
    def atualizar_patch_cliente(cliente_id, cliente_data):
        if not cliente_data: raise ClientException("Nenhum dado fornecido")

        cliente = ClientService._get_cliente_or_404(cliente_id)

        ClientService._update_fields(cliente, cliente_data)

        db.session.commit()
        return ReturnClients.clients(cliente)
