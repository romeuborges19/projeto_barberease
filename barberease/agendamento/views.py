from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from agendamento.forms import AgendaForm
from agendamento.models import Agenda

# Create your views here.

class CadastrarAgendaView(CreateView):
    form_class = AgendaForm
    model = Agenda
    template_name = "agenda_cadastro.html"

    def get(self, request, *args, **kwargs):
        if not self.request.session['dono']:
            print("USUARIO NÃO É DONO")
            return redirect(reverse_lazy("usuario:home"))

        return super().get(request, *args, **kwargs)

