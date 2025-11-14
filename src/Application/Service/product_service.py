from src.Infrastructure.models.produto import Produto
from src.utils.return_service import ReturnProducts
from src import db

class ProductException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

class ProductService:

    @staticmethod
    def _get_produto_or_404(produto_id):
        produto = Produto.query.get(produto_id)
        if not produto: raise ProductException("Produto não encontrado")
        return produto

    @staticmethod
    def _parse_preco(preco):
        try:
            return float(preco)
        except:
            raise ProductException("O campo 'preco' deve ser numérico")

    @staticmethod
    def _update(produto, dados):
        for campo, valor in dados.items():
            if valor is None: continue

            if campo == "preco":
                valor = ProductService._parse_preco(valor)

            setattr(produto, campo, valor)

    @staticmethod
    def cadastrar_produto(produto_data):
        if not produto_data: raise ProductException("Nenhum dado fornecido")

        for campo in ["nome", "preco"]:
            if not produto_data.get(campo): raise ProductException(f"Passe um valor para o campo '{campo}'")

        novo = Produto(
            nome=str(produto_data["nome"]),
            preco=ProductService._parse_preco(produto_data["preco"])
        )

        db.session.add(novo)
        db.session.commit()

        return ReturnProducts.products(novo)

    @staticmethod
    def listar_produtos():
        produtos = Produto.query.all()
        if not produtos: raise ProductException("Não foram encontrados produtos cadastrados")
        return [ReturnProducts.products(p) for p in produtos]

    @staticmethod
    def listar_produto_id(produto_id):
        produto = ProductService._get_produto_or_404(produto_id)
        return ReturnProducts.products(produto)

    @staticmethod
    def deletar_produto(produto_id):
        produto = ProductService._get_produto_or_404(produto_id)
        db.session.delete(produto)
        db.session.commit()

    @staticmethod
    def atualizar_produto(produto_id, produto_data):
        if not produto_data: raise ProductException("Nenhum dado fornecido")

        produto = ProductService._get_produto_or_404(produto_id)

        for campo in ["nome", "preco"]:
            if not produto_data.get(campo): raise ProductException(f"Passe um valor para o campo '{campo}'")

        dados = produto_data.copy()
        ProductService._update(produto, dados)

        db.session.commit()
        return ReturnProducts.products(produto)

    @staticmethod
    def atualizar_patch_produto(produto_id, produto_data):
        if not produto_data: raise ProductException("Nenhum dado fornecido")

        produto = ProductService._get_produto_or_404(produto_id)
        ProductService._update(produto, produto_data)

        db.session.commit()
        return ReturnProducts.products(produto)
