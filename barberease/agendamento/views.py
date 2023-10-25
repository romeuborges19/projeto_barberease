from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from agendamento.forms import AgendaForm
from agendamento.models import Agenda
from barbearia.models import Barbearia

# Create your views here.

class CadastrarAgendaView(CreateView):
    form_class = AgendaForm
    model = Agenda
    template_name = "agenda_cadastro.html"

    def get(self, request, *args, **kwargs):
        if not self.request.session['dono']:
            return redirect(reverse_lazy("usuario:home"))
        else:
            usuario = self.request.user

            if not Barbearia.objects.filter(dono=usuario).exists():
                # TODO: Criar tela que avisa ao usuário que o usuário 
                # deve cadastrar sua barbearia antes de cadastrar sua agenda

                return redirect(reverse_lazy("barbearia:cadastrar_barbearia"))

        return super().get(request, *args, **kwargs)

