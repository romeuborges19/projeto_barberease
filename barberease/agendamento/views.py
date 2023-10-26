from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
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

class AgendaView(TemplateView):
    template_name = "agenda.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['agenda'] = Agenda.objects.get(id=kwargs['pk'])
