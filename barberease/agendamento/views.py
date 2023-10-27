from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from agendamento.forms import AgendaForm
from agendamento.models import Agenda
from barbearia.models import Barbearia

# Create your views here.

class CadastrarAgendaView(CreateView):
    form_class = AgendaForm
    model = Agenda
    template_name = "agenda_cadastro.html"
    success_url = reverse_lazy("agendamento:agenda")

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
        agenda = Agenda.objects.get(barbearia_id=self.request.session['id_barbearia'])
        return super().get_success_url()

class AgendaView(DetailView):
    template_name = "agenda.html"

    def get_queryset(self):
        self.agenda = get_object_or_404(Agenda, id=self.kwargs['pk'])

        return Agenda.objects.filter(id=self.agenda.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        agenda = Agenda.objects.get(id=self.agenda.id)
        context['agenda'] = agenda

        coluna_horarios = []
        horarios_context = []

        for dia, horarios in agenda.horarios_funcionamento.items():
            for horario in horarios:
                if horario not in coluna_horarios:
                        coluna_horarios.append(horario)

            coluna_horarios = sorted(coluna_horarios)

        row_hora = {}
        for hora in coluna_horarios:
            row = []
            for dia, horarios in agenda.horarios_funcionamento.items():
                if hora in horarios:
                    row.append("X")
                else: row.append("-")
            row_hora[f"{hora}"] = row
        
        print(f'coluna p/ hora = {row_hora}')

        context['coluna_horarios'] = coluna_horarios
        context['horarios_disponiveis'] = row_hora

        return context

    def get_object(self):
        agenda = super().get_object()

        return agenda
