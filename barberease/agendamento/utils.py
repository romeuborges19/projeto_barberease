from datetime import datetime, timedelta

from agendamento.models import Agendamento


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
        dias_semana.append(weekday.date().strftime("%d-%m-%Y"))

    return dias_semana

class Celula:
    def __init__(self, dia, hora, funciona):
        self.dia = dia
        self.hora = hora 
        self.hora_slug = datetime.strptime(hora, "%H:%M").strftime("%H-%M")
        self.hora_hora = hora.strip(':00')
        self.funciona = funciona

    def get_agendamentos(self):
        dia = datetime.strptime(self.dia, "%d-%m-%Y").strftime("%Y-%m-%d")
        self.agendamentos = Agendamento.objects.filter(data__date=dia, data__hour=self.hora_hora)
        return self.agendamentos

    def get_disponibilidade(self):
        tempo_total = 0
        for agendamento in self.agendamentos:
            tempo_total = tempo_total + agendamento.servico.tempo_servico

        if tempo_total >= 60:
            self.disponivel = False
        else:
            self.disponivel = True

