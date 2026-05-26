from src.Infrastructure.models.admin import Admin
from src.utils.return_service import ReturnAdmin
from src.utils.auth import AuthUtils, AuthTokenException
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
    def _validate_required_string_fields(data, fields, exception_cls):
        for campo in fields:
            valor = data.get(campo)
            if not valor:
                raise exception_cls(f"Passe um valor para o campo '{campo}'")
            if not isinstance(valor, str):
                raise exception_cls(f"Passe o valor do campo '{campo}' em String")

    @staticmethod
    def _validate_unique_fields(cpf, email, current_admin_id=None):
        cpf_query = Admin.query.filter_by(cpf=cpf).first()
        if cpf_query and cpf_query.id != current_admin_id:
            raise AdminException("Já existe um admin cadastrado com esse CPF")

        email_query = Admin.query.filter_by(email=email).first()
        if email_query and email_query.id != current_admin_id:
            raise AdminException("Já existe um admin cadastrado com esse email")

    @staticmethod
    def _authenticate_admin(cpf, senha):
        admin = Admin.query.filter_by(cpf=cpf).first()
        if not admin:
            raise LoginException("CPF incorreto")

        if not bcrypt.checkpw(senha.encode('utf-8'), admin.senha.encode('utf-8')):
            raise LoginException("Senha incorreta")

        return admin

    @staticmethod
    def _build_auth_response(admin):
        admin_payload = ReturnAdmin.admins(admin)
        return AuthUtils.build_auth_payload(admin, admin_payload)
    
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

        AdminService._validate_required_string_fields(
            admin_data,
            ["nome", "cpf", "email", "celular", "senha"],
            AdminException,
        )

        AdminService._validate_unique_fields(admin_data["cpf"], admin_data["email"])

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
    def registrar_admin(admin_data):
        if not admin_data:
            raise AdminException("Nenhum dado fornecido")

        AdminService._validate_required_string_fields(
            admin_data,
            ["nome", "cpf", "email", "celular", "senha"],
            AdminException,
        )

        admin_data_normalized = {
            "nome": admin_data["nome"].strip(),
            "cpf": admin_data["cpf"].strip(),
            "email": admin_data["email"].strip().lower(),
            "celular": admin_data["celular"].strip(),
            "senha": admin_data["senha"],
        }

        AdminService._validate_unique_fields(
            admin_data_normalized["cpf"],
            admin_data_normalized["email"],
        )

        senha_crypt = bcrypt.hashpw(
            admin_data_normalized["senha"].encode('utf-8'),
            bcrypt.gensalt(),
        ).decode('utf-8')

        admin = Admin(
            nome=admin_data_normalized["nome"],
            cpf=admin_data_normalized["cpf"],
            email=admin_data_normalized["email"],
            celular=admin_data_normalized["celular"],
            senha=senha_crypt,
        )

        db.session.add(admin)
        db.session.commit()

        return AdminService._build_auth_response(admin)
    
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

        AdminService._validate_unique_fields(admin_data["cpf"], admin_data["email"], admin.id)

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

        AdminService._validate_required_string_fields(
            admin_data,
            ['cpf', 'senha'],
            LoginException,
        )

        admin = AdminService._authenticate_admin(
            admin_data['cpf'].strip(),
            admin_data['senha'],
        )
        return AdminService._build_auth_response(admin)

    @staticmethod
    def refresh_login(refresh_token):
        if not refresh_token:
            raise LoginException("Refresh token não informado")

        try:
            payload = AuthUtils.decode_token(refresh_token, "refresh")
            admin = AdminService._get_admin_or_404(int(payload["sub"]))
        except (AuthTokenException, ValueError) as exc:
            raise LoginException(str(exc)) from exc

        return AdminService._build_auth_response(admin)

    @staticmethod
    def get_admin_autenticado(access_token):
        if not access_token:
            raise LoginException("Token não informado")

        try:
            payload = AuthUtils.decode_token(access_token, "access")
            admin = AdminService._get_admin_or_404(int(payload["sub"]))
        except (AuthTokenException, ValueError) as exc:
            raise LoginException(str(exc)) from exc

        return ReturnAdmin.admins(admin)
