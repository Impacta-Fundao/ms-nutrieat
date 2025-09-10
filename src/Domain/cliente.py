from datetime import date
class ClientDomain:
    def __init__(self, nome, cpf, data_nascimento):
        self.nome = nome
        self.cpf = cpf     
        self.data_nascimento = data_nascimento     
    
    def calcularIdade(self):
        
        hoje = date.today()
        mes = self.data_nascimento.split('-')[1]
        idade = hoje.year - self.data_nascimento.split('-')[0] #2006-06-20
        if (hoje.month, hoje.day) < (idade[1], idade[2]):
            idade
        
