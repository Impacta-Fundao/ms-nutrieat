from datetime import date
def calcularIdade(data_nascimento):
        stringData = str(data_nascimento)
        hoje = date.today()
        mes = int(stringData.split('-')[1])
        dia = int(stringData.split('-')[2])
        ano = int(stringData.split('-')[0])
        idade = hoje.year - ano #[2006]-[06]-[20]
        if len(str(ano)) == 4:
            if mes <= 12 and dia <= 30: 
                if (hoje.month, hoje.day) < (mes, dia):
                    idade-=1
                return idade 
            raise Exception("Data inválida")
        raise Exception("Formato inválido do campo: data_nascimento")
    
    
