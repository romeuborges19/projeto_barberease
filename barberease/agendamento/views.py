from datetime import datetime
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from agendamento.forms import AgendaForm, AgendamentoForm, ServicoForm
from agendamento.models import Agenda, Agendamento, Servico
from agendamento.utils import Celula, get_dias_semana, semana_sort
from barbearia.models import Barbearia
from usuarios.authentication import get_token_user_id

# Create your views here.

class RealizarAgendamentoView(CreateView):
    model = Agendamento
    form_class = AgendamentoForm
    template_name = "agendamento.html"
    success_url = reverse_lazy("usuario:home")

    def get_form_kwargs(self):
        queryset = Servico.objects.filter(barbearia_id=self.kwargs['pk'])

        form_kwargs = super(RealizarAgendamentoView, self).get_form_kwargs()
        form_kwargs['servico_queryset'] = queryset

        return form_kwargs

    def form_valid(self, form):
        form.instance.agenda = Agenda.objects.get(id=self.kwargs['pk'])

        print(f"{self.kwargs['hora']}")
        hora = self.kwargs['hora'].strip('00')
        print(f"{hora}")

        hora = hora + f"{form.cleaned_data.get('minuto')}"
        print(f"{hora}")
        
        data = f"{self.kwargs['dia']} {hora}"
        form.instance.data = datetime.strptime(data, "%d-%m-%Y %H-%M")
        form.instance.aprovado = False
        form.instance.cliente = self.request.user

        return super().form_valid(form)

class CadastrarServicoView(CreateView):
    model = Servico
    form_class = ServicoForm
    template_name = "servico_cadastro.html"
    success_url = reverse_lazy("barbearia:home")

    def form_valid(self, form):
        id_usuario = get_token_user_id(self.request)
        form.instance.barbearia = Barbearia.objects.get(dono_id=id_usuario)

        return super().form_valid(form)
    
    def get_success_url(self):
        id_usuario = get_token_user_id(self.request)
        id_barbearia = Barbearia.objects.values_list('id', flat=True).get(dono_id=id_usuario)
        return reverse_lazy("barbearia:home", kwargs={'pk': id_barbearia}) 

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

        dias_semana = get_dias_semana()
        context['dias_semana'] = get_dias_semana()
        
        for dia, horarios in agenda.horarios_funcionamento.items():
            for horario in horarios:
                if horario not in coluna_horarios:
                    coluna_horarios.append(horario)

            coluna_horarios = sorted(coluna_horarios)

        # Gerando as linhas que renderizam os horários em suas posições na agenda
        linha_horarios = {}
        for hora in coluna_horarios:
            i = 0
            row = []
            for dia, horarios in agenda.horarios_funcionamento.items():
                if hora in horarios:
                    row.append(Celula(dias_semana[i], hora, "Testando"))
                else: 
                    row.append(Celula(dias_semana[i], hora, "-------"))
                i = i + 1

            linha_horarios[f"{hora}"] = row
        
        context['coluna_horarios'] = coluna_horarios
        context['linha_horarios'] = linha_horarios

        return context

    def get_object(self):
        agenda = super().get_object()

        return agenda

class AgendaAgendamentoView(DetailView):
    model = Agenda
    template_name = "agenda_agendamento.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        agenda = self.object
        context['agenda'] = agenda 

        # Gerando uma lista que armazena os horários disponíveis da barbearia, 
        # sem repetir valores
        coluna_horarios = []

        agenda.horarios_funcionamento = semana_sort(agenda.horarios_funcionamento.items())

        dias_semana = get_dias_semana()
        context['dias_semana'] = get_dias_semana()
        
        for dia, horarios in agenda.horarios_funcionamento.items():
            for horario in horarios:
                if horario not in coluna_horarios:
                    coluna_horarios.append(horario)

            coluna_horarios = sorted(coluna_horarios)

        # Gerando as linhas que renderizam os horários em suas posições na agenda
        linha_horarios = {}
        for hora in coluna_horarios:
            i = 0
            row = []
            for dia, horarios in agenda.horarios_funcionamento.items():
                if hora in horarios:
                    hora = datetime.strptime(f"{hora}", "%H:%M").strftime("%H:%M")
                    celula = Celula(dias_semana[i], hora, True)
                    celula.get_agendamentos()
                    celula.get_disponibilidade()
                    row.append(celula)
                else: 
                    row.append(Celula(dias_semana[i], hora, False))
                i = i + 1

            linha_horarios[f"{hora}"] = row
        
        context['coluna_horarios'] = coluna_horarios
        context['linha_horarios'] = linha_horarios

        return context

    def get_object(self):
        agenda = Agenda.objects.get(barbearia_id=self.kwargs['pk']) 

        return agenda
