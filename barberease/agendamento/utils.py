from datetime import datetime, timedelta
from django.db.models import Q
from agendamento.models import Agenda, Agendamento
from barbearia.models import Barbearia, Barbeiros
from usuarios.authentication import get_token_user_id
from usuarios.models import Usuario

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

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

def get_menu_data_context(request, context):
    context['usuario'] = request.user

    if request.user.dono_barbearia:
        barbearia = Barbearia.objects.filter(dono=request.user).first()
        agenda = Agenda.objects.filter(barbearia=barbearia).first()

        context['barbearia'] = barbearia
        context['id_agenda'] = agenda.pk

        barbeiros = Barbeiros.objects.filter(barbearia=barbearia)
        context['barbeiros'] = barbeiros

    return context

class Celula:
    def __init__(self, dia, hora, funciona):
        self.dia = dia
        self.hora = hora 
        self.hora_slug = datetime.strptime(hora, "%H:%M").strftime("%H-%M")
        self.hora_hora = hora.strip(':00') 
        self.funciona = funciona

        if int(self.hora_hora) < 10:
            self.hora_hora = '0' + self.hora_hora

    def get_agendamentos(self, agendamentos):
        #TODO: Otimizar esta função
        dia = self.dia

        # self.agendamentos = Agendamento.objects.filter(
        #     data__date=dia, data__hour=self.hora_hora,
        #     agenda_id=agenda_id,
        #     aprovado=True,
        # ).order_by('data')

        self.agendamentos = []

        for agendamento in agendamentos:
            if agendamento.data.date().strftime("%Y-%m-%d") == dia and agendamento.data.strftime("%H") == self.hora_hora:
                self.agendamentos.append(agendamento)

        for agendamento in self.agendamentos:
            agendamento.hora_inicio = agendamento.data.strftime("%H:%M")
            agendamento.hora_fim = agendamento.hora_fim.strftime("%H:%M")

        return self.agendamentos

    def get_disponibilidade(self):
        excedentes = Agendamento.objects.filter(
            ~Q(data__hour=self.hora_hora),
            hora_fim__hour=self.hora_hora,
        )

        tempo_total = 0

        if not excedentes:
            for agendamento in excedentes:
                minutos = int(self.hora.strip(f"{self.hora_hora}:"))
                minutos_faltantes = 60 - minutos
                tempo = int(agendamento.servico.tempo_servico) - minutos_faltantes
                tempo_total = tempo_total + tempo

        for agendamento in self.agendamentos:
            hora_fim = agendamento.hora_fim.split(':')[0]

            if hora_fim != self.hora_hora:
                tempo_total = tempo_total + (agendamento.servico.tempo_servico - (int(hora_fim) + 1))
            else:
                tempo_total = tempo_total + agendamento.servico.tempo_servico

        if tempo_total >= 60:
            self.disponivel = False
        else:
            self.disponivel = True

