from datetime import date
class ClientDomain:
    def __init__(self, nome, cpf, data_nascimento, numero, turno, sala, email):
        self.nome = nome
        self.cpf = cpf     
        self.data_nascimento = data_nascimento
        self.turno = turno
        self.numero = numero
        self.sala = sala
        self.email = email
    

        