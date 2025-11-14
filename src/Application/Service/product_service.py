from src.Infrastructure.models.produto import Produto
from src.utils.return_service import ReturnProducts
from src import db

class ProductException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

class ProductService:
    
    @staticmethod
    def cadastrar_produto(produto_data):
        if not produto_data: raise ProductException("Nenhum dado fornecido")

        if not produto_data.get("nome"): raise ProductException("Passe um valor para o campo 'nome'")
        if not produto_data.get("preco"): raise ProductException("Passe um valor para o campo 'preco'")
                    
        novo_produto = Produto(nome=str(produto_data["nome"]), preco=float(produto_data["preco"]))

        db.session.add(novo_produto)
        db.session.commit()

        novo_produto = Produto.query.order_by(Produto.id.desc()).first()

        return ReturnProducts.products(novo_produto)
    
    @staticmethod
    def listar_produtos():
        produtos = Produto.query.all()

        if not produtos: raise ProductException("Não foram encontrados produtos cadastrados")

        return [ReturnProducts.products(produto) for produto in produtos]
    
    @staticmethod
    def listar_produto_id(produto_id):
        produto = Produto.query.get(produto_id)

        if not produto: raise ProductException("Produto não encontrado")

        return ReturnProducts.products(produto)
    
    @staticmethod
    def deletar_produto(produto_id):
        produto = Produto.query.get(produto_id)

        if not produto: raise ProductException("Produto não encontrado")
        
        db.session.delete(produto)
        db.session.commit()
    
    @staticmethod
    def atualizar_produto(produto_id, produto_data):
        if not produto_data: raise ProductException("Nenhum dado fornecido")

        produto = Produto.query.get(produto_id)

        if not produto: raise ProductException("Produto não encontrado")
        
        if not produto_data.get("nome"): raise ProductException("Passe um valor para o campo 'nome'")
        if not produto_data.get("preco"): raise ProductException("Passe um valor para o campo 'preco'")
        
        produto.nome = produto_data["nome"]
        produto.preco = produto_data["preco"]
    
        db.session.commit()
        
        return ReturnProducts.products(produto)
        
    @staticmethod
    def atualizar_patch_produto(produto_id, produto_data):
        if not produto_data: raise ProductException("Nenhum dado fornecido")

        produto = Produto.query.get(produto_id)

        if not produto: raise ProductException("Produto não encontrado")

        if produto_data.get("nome"): produto.nome = produto_data["nome"]
        if produto_data.get("preco"): produto.preco = produto_data["preco"]
            
        db.session.commit()
        
        return ReturnProducts.products(produto)
