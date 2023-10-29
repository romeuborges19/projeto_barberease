from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from agendamento.forms import AgendaForm
from agendamento.models import Agenda
from agendamento.utils import semana_sort
from barbearia.models import Barbearia

# Create your views here.

class CadastrarAgendaView(CreateView):
    form_class = AgendaForm
    model = Agenda
    template_name = "agenda_cadastro.html"

    def get(self, request, *args, **kwargs):
        if not Barbearia.objects.get(dono=self.request.user):
            return redirect(reverse_lazy("usuario:home"))
        # else:
        #     usuario = self.request.user

        #     if not Barbearia.objects.filter(dono=usuario).exists():
        #         # TODO: Criar tela que avisa ao usuário que o usuário 
        #         # deve cadastrar sua barbearia antes de cadastrar sua agenda

        #         return redirect(reverse_lazy("barbearia:cadastrar_barbearia"))

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        barbearia = Barbearia.objects.get(pk=self.request.session['id_barbearia'])
        form.instance.barbearia = barbearia

        return super().form_valid(form)

    def get_success_url(self):
        agenda_id = Agenda.objects.values_list('id', flat=True).get(barbearia_id=self.request.session['id_barbearia'])
        return reverse_lazy("agendamento:agenda", kwargs={'pk':agenda_id})

class AgendaView(DetailView):
    model = Agenda
    template_name = "agenda.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        agenda = self.object
        context['agenda'] = agenda 

        # Gerando uma lista que armazena os horários disponíveis da barbearia, 
        # sem repetir valores
        coluna_horarios = []

        agenda.horarios_funcionamento = semana_sort(agenda.horarios_funcionamento.items())

        for dia, horarios in agenda.horarios_funcionamento.items():
            for horario in horarios:
                if horario not in coluna_horarios:
                        coluna_horarios.append(horario)

            coluna_horarios = sorted(coluna_horarios)

        # Gerando as linhas que renderizam os horários em suas posições na agenda
        linha_horarios = {}
        for hora in coluna_horarios:
            row = []
            for dia, horarios in agenda.horarios_funcionamento.items():
                if hora in horarios:
                    row.append("Hora")
                else: row.append("--")
            linha_horarios[f"{hora}"] = row
        
        context['coluna_horarios'] = coluna_horarios
        context['linha_horarios'] = linha_horarios

        return context

    def get_object(self):
        agenda = super().get_object()

        return agenda



