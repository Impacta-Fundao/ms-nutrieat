from datetime import date

def calcular_idade(data_nascimento):
    if isinstance(data_nascimento, str):
        
        dia_nascimento = int(data_nascimento.split('-')[2])
        mes_nascimento = int(data_nascimento.split('-')[1])
        ano_nascimento = int(data_nascimento.split('-')[0])

        hoje = date.today()
        idade = hoje.year - ano_nascimento

        if (hoje.month, hoje.day) < (mes_nascimento, dia_nascimento):
            idade -= 1

        return idade
