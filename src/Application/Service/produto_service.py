from src.Domain.produto import ProdutoDomain
from src.Infrastructure.models.produto import Produto
from src import db

class ProdutoException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

class ProdutoService:
    
    @staticmethod
    def create_produto(nome,preco):
        new_produto = ProdutoDomain(nome,preco)
        produto = Produto(nome=new_produto.nome,preco=new_produto.preco)
        db.session.add(produto)
        db.session.commit()
        return produto
    
    @staticmethod
    def listar_produtos():
        data = Produto.query.all()
        produto_json = [{
            'id': produto.id,
            'nome': produto.nome,
            'preço': produto.preco,
        } for produto in data]
        
        return produto_json
    
    @staticmethod
    def get_id(produto_id):
        data = Produto.query.get(produto_id)

        if data is None: raise ProdutoException("Esse produto não está cadastrado")
        produto_json = {
            'id': data.id,
            'nome': data.nome,
            'preço': data.preco,
        } 
        
        return produto_json
    
    @staticmethod
    def deletar_produto(produto_id):
        data = Produto.query.get(produto_id)
        if data is None:return None
        
        db.session.delete(data)
        db.session.commit()
        return {"message": "Produto deletado com sucesso"}
    
    @staticmethod
    def atualizar_produto(produto_id, produto_data):
        data = Produto.query.get(produto_id)
        if data is None:
            raise ProdutoException("produto não encontrado")
        
        required_fields = {
            'nome': produto_data.get('nome'),
            'preco': produto_data.get('preco')
        }
        
        for field, value in required_fields.items():
            if value is None:
                raise ProdutoException(f"Passe um valor para o campo {field}")
        
        data.nome = required_fields['nome']
        data.preco = required_fields['preco']
    
        
        db.session.commit()
        
        return {
            'id': data.id,
            'nome': data.nome,
            'preço': data.preco
        }
        
    @staticmethod
    def atualizar_patch_produto(produto_id, produto_data):
        data = Produto.query.get(produto_id)
        if data is None:
            raise ProdutoException("produto não encontrado")
        if produto_data.get('nome'):
            data.nome = produto_data['nome']
        if produto_data.get('preco'):
            data.preco = produto_data['preco']
            
        db.session.commit()
        
        return {
            'id': data.id,
            'nome': data.nome,
            'preço': data.preco
        }
