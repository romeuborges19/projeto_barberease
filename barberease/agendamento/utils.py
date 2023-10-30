from datetime import datetime, timedelta


def semana_sort(dicionario):
    semana = ['segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sabado', 'domingo']

    novo_dicionario = {}
    for i in range(0, 7):
        for dia, horarios in dicionario:
            if dia == semana[i]:
                novo_dicionario[dia] = horarios

    return novo_dicionario

def get_dias_semana():
    hoje = datetime.now()
    segunda = hoje - timedelta(days=hoje.weekday())
    dias_semana = []

    for i in range(0, 7):
        weekday = segunda + timedelta(days = (segunda.weekday() + i))
        dias_semana.append(weekday.date().strftime("%d/%m/%Y"))

    return dias_semana

class Celula:
    def __init__(self, dia, hora, conteudo):
        self.dia = dia
        self.hora = datetime.strptime(hora, "%H:%M").time()
        self.conteudo = conteudo
