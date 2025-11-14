from src.Infrastructure.models.admin import Admin
from src.utils.return_service import ReturnAdmin
from src import db
import bcrypt

class AdminException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

class LoginException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

class AdminService:

    @staticmethod
    def _get_admin_or_404(admin_id):
        admin = Admin.query.get(admin_id)
        if not admin: raise AdminException("Admin não encontrado")
        return admin
    
    @staticmethod
    def _update_fields(admin, dados):
        for campo, valor in dados.items():
            if valor is None: continue
            if not isinstance(valor, str): raise AdminException(f"Passe o valor do campo '{campo}' em String")
            if campo == "senha": valor = bcrypt.hashpw(valor.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            setattr(admin, campo, valor)

    @staticmethod
    def criar_admin(admin_data):
        if not admin_data: raise AdminException("Nenhum dado fornecido")

        for campo in ["nome", "cpf", "email", "celular", "senha"]:
            if not admin_data.get(campo): raise AdminException(f"Passe um valor para o campo '{campo}'")
            if not isinstance(admin_data.get(campo), str): raise AdminException(f"Passe o valor do campo '{campo}' em String")

        senha_crypt = bcrypt.hashpw(admin_data["senha"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        admin = Admin(
            nome=admin_data["nome"],
            cpf=admin_data["cpf"],
            email=admin_data["email"],
            celular=admin_data["celular"],
            senha=senha_crypt
        )

        db.session.add(admin)
        db.session.commit()

        return ReturnAdmin.admins(admin)
    
    @staticmethod
    def listar_admins():
        admins = Admin.query.all()
        if not admins: raise AdminException("Não foram encontrados admins cadastrados")
        return [ReturnAdmin.admins(a) for a in admins]

    @staticmethod
    def get_id(admin_id):
        admin = AdminService._get_admin_or_404(admin_id)
        return ReturnAdmin.admins(admin)
    
    @staticmethod
    def deletar_admin(admin_id):
        admin = AdminService._get_admin_or_404(admin_id)
        db.session.delete(admin)
        db.session.commit()

    @staticmethod
    def atualizar_admin(admin_id, admin_data):
        if not admin_data: raise AdminException("Nenhum dado fornecido")

        admin = AdminService._get_admin_or_404(admin_id)

        for campo in ["nome", "cpf", "email", "celular", "senha"]:
            if not admin_data.get(campo): raise AdminException(f"O campo '{campo}' é obrigatório")

        dados = admin_data.copy()

        AdminService._update_fields(admin, dados)
        
        db.session.commit()

        return ReturnAdmin.admins(admin)
    
    @staticmethod
    def atualizar_patch_admin(admin_id, admin_data):
        if not admin_data: raise AdminException("Nenhum dado fornecido")

        admin = AdminService._get_admin_or_404(admin_id)

        AdminService._update_fields(admin, admin_data)

        db.session.commit()

        return ReturnAdmin.admins(admin)

    @staticmethod
    def login_admin(admin_data):
        if not admin_data: raise LoginException("Nenhum dado fornecido")
        
        for campo in ['cpf', 'senha']:
            if not admin_data.get(campo): raise LoginException(f"Passe um valor para o campo {campo}")

        admin = Admin.query.filter_by(cpf=admin_data['cpf']).first()
        if not admin: raise LoginException("CPF incorreto")

        senha = admin.senha
        
        if bcrypt.checkpw(admin_data['senha'].encode('utf-8'), senha.encode('utf-8')): return admin.nome
        else: raise LoginException("Senha incorreta")
