from datetime import date
def calcularIdade(data_nascimento):
        
        hoje = date.today()
        mes = int(data_nascimento.split('-')[1])
        dia = int(data_nascimento.split('-')[2])
        ano = int(data_nascimento.split('-')[0])
        idade = hoje.year - ano #[2006]-[06]-[20]
        if (hoje.month, hoje.day) < (mes, dia):
            idade-=1
        return idade