from datetime import date, datetime, timedelta
from typing import Any
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
import time

from agendamento.forms import AgendaForm, AgendamentoForm, ServicoForm
from agendamento.models import Agenda, Agendamento, Servico, Barbeiros
from agendamento.utils import Celula, get_dias_semana, get_dias_semana_simplificado, get_menu_data_context, is_ajax, semana_sort
from barbearia.models import Barbearia

DIAS = (
    (0, "Segunda-feira"),
    (1, "Terça-feira"),
    (2, "Quarta-feira"),
    (3, "Quinta-feira"),
    (4, "Sexta-feira"),
    (5, "Sábado"),
    (6, "Domingo")
)

# Create your views here.

class RealizarAgendamentoView(CreateView):
    model = Agendamento
    form_class = AgendamentoForm
    template_name = "agendamento_cadastro.html"

    def get_success_url(self):
        usuario_id = self.request.user.id
        return reverse_lazy("usuario:home", kwargs={'pk': usuario_id})

    def get_form_kwargs(self):
        queryset = Servico.objects.filter(barbearia_id=self.kwargs['pk'])

        form_kwargs = super(RealizarAgendamentoView, self).get_form_kwargs()
        form_kwargs['servico_queryset'] = queryset

        return form_kwargs

    def form_valid(self, form):
        form.instance.agenda = Agenda.objects.get(id=self.kwargs['pk'])

        hora = self.kwargs['hora'].strip('00')
        hora = hora + f"{form.cleaned_data.get('minuto')}"

        hora_inicio = datetime.strptime(hora, "%H-%M")
        
        servico = form.cleaned_data.get('servico')
        hora_fim = hora_inicio + timedelta(minutes=servico.tempo_servico)
        
        data = f"{self.kwargs['dia']} {hora}"
        form.instance.data = datetime.strptime(data, "%d-%m-%Y %H-%M")
        form.instance.hora_fim = hora_fim.time()
        form.instance.aprovado = False
        form.instance.cliente = self.request.user

        return super().form_valid(form)

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
        usuario = self.request.user
        barbearia = Barbearia.objects.filter(dono=usuario).first()
        form.instance.barbearia = barbearia  

        return super().form_valid(form)

    def get_success_url(self):
        usuario = self.request.user
        barbearia = Barbearia.objects.filter(dono=usuario).first()
        agenda = Agenda.objects.filter(barbearia=barbearia.id).first()

        return reverse_lazy("agendamento:agenda", kwargs={'pk':agenda.id})

class AgendaBarbeariaView(DetailView):
    model = Agenda
    template_name = "agenda_barbearia.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        agenda = self.object
        context['agenda'] = agenda 

        # Gerando uma lista que armazena os horários disponíveis da barbearia, 
        # sem repetir valores
        coluna_horarios = []

        agenda.horarios_funcionamento = semana_sort(agenda.horarios_funcionamento.items())
        dias_semana = get_dias_semana()
        context['dias_semana'] = get_dias_semana_simplificado()
        dias_semana[0] = datetime.strptime(dias_semana[0], "%d-%m-%Y").strftime("%Y-%m-%d")
        dias_semana[-1] = datetime.strptime(dias_semana[-1], "%d-%m-%Y").strftime("%Y-%m-%d")
        
        agendamentos = Agendamento.objects.filter(
            data__date__range=(dias_semana[0], dias_semana[-1]), 
            agenda_id=agenda.pk, 
            aprovado=True)

        print(agendamentos)
        
        for _, horarios in agenda.horarios_funcionamento.items():
            for horario in horarios:
                if horario not in coluna_horarios:
                    coluna_horarios.append(horario)

        coluna_horarios = sorted(coluna_horarios)

        # Gerando as linhas que renderizam os horários em suas posições na agenda
        linha_horarios = {}
        for hora in coluna_horarios:
            i = 0
            row = []
            for _, horarios in agenda.horarios_funcionamento.items():
                if hora in horarios:
                    celula = Celula(dias_semana[i], hora, True)
                    celula.get_agendamentos(agendamentos)
                    row.append(celula)
                else: 
                    row.append(Celula(dias_semana[i], hora, False))
                i = i + 1

            linha_horarios[f"{hora}"] = row
        
        context['coluna_horarios'] = coluna_horarios
        context['linha_horarios'] = linha_horarios

        context = get_menu_data_context(self.request, context)

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
        print(agenda.pk)

        # Gerando uma lista que armazena os horários disponíveis da barbearia, 
        # sem repetir valores
        coluna_horarios = []

        agenda.horarios_funcionamento = semana_sort(agenda.horarios_funcionamento.items())

        dias_semana = get_dias_semana()
        context['dias_semana'] = dias_semana
        primero_dia_semana = datetime.strptime(dias_semana[0], "%d-%m-%Y").strftime("%Y-%m-%d")
        ultimo_dia_semana = datetime.strptime(dias_semana[-1], "%d-%m-%Y").strftime("%Y-%m-%d")

        agendamentos = Agendamento.objects.filter(
            data_date_range=(primero_dia_semana, ultimo_dia_semana), 
            agenda_id=agenda.pk, aprovado=True)

        print(agendamentos)
        
        for _, horarios in agenda.horarios_funcionamento.items():
            for horario in horarios:
                if horario not in coluna_horarios:
                    coluna_horarios.append(horario)

        coluna_horarios = sorted(coluna_horarios)

        # Gerando as linhas que renderizam os horários em suas posições na agenda
        linha_horarios = {}
        for hora in coluna_horarios:
            i = 0
            row = []
            for _, horarios in agenda.horarios_funcionamento.items():
                if hora in horarios:
                    hora = datetime.strptime(f"{hora}", "%H:%M").strftime("%H:%M")
                    celula = Celula(dias_semana[i], hora, True)
                    celula.get_agendamentos(agendamentos)
                    celula.get_disponibilidade()
                    print(celula.disponivel)
                    row.append(celula)
                else: 
                    row.append(Celula(dias_semana[i], hora, False))
                i = i + 1

            linha_horarios[f"{hora}"] = row
        
        context['coluna_horarios'] = coluna_horarios
        context['linha_horarios'] = linha_horarios

        context = get_menu_data_context(self.request, context)

        return context

    def get_object(self):
        agenda = super().get_object()
        return agenda

# Views de Serviço

class CadastrarServicoView(CreateView):
    # Views para renderizar a tela de cadastro de Serviço
    
    model = Servico
    form_class = ServicoForm
    template_name = "servico_cadastro.html"
    success_url = reverse_lazy("agendamento:listar_servicos")

    def form_valid(self, form):
        user = self.request.user
        barbearia = Barbearia.objects.filter(dono=user).first()
        form.instance.barbearia = barbearia
        return super().form_valid(form)
    
    def get_context_data(self, *, object_list=None, **kwargs):  
        context = super().get_context_data(object_list=object_list, **kwargs)
        context = get_menu_data_context(self.request, context)
        return context

class ListarServicosView(ListView):
    # Views para renderizar a tela de listagem de Serviços
    
    model = Servico
    template_name = 'servicos_listagem.html'
    paginate_by = 10

    def get_queryset(self):
        barbearia = self.request.user.barbearia
        servicos = Servico.objects.filter(barbearia_id=barbearia.id)
        return servicos
    
    def get_context_data(self, *, object_list=None, **kwargs):  
        context = super().get_context_data(object_list=object_list, **kwargs)
        context = get_menu_data_context(self.request, context)
        return context
    
class DeletarServicoView(DeleteView):
    # Views para renderizar a tela de deletar Serviço
    
    model = Servico
    success_url = reverse_lazy("agendamento:listar_servicos")
    template_name = 'servico_deletar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_menu_data_context(self.request, context)
        return context
    
class EditarServicoView(UpdateView):
    # Views para renderizar a tela de edição de Serviço
    
    model = Servico
    form_class = ServicoForm
    template_name = "servico_editar.html"
    success_url = reverse_lazy("agendamento:listar_servicos")
    
    def form_valid(self, form):
        user = self.request.user
        barbearia = Barbearia.objects.filter(dono=user).first()
        form.instance.barbearia = barbearia
        return super().form_valid(form)
    
    def get_context_data(self, *, object_list=None, **kwargs):  
        context = super().get_context_data(object_list=object_list, **kwargs)
        context = get_menu_data_context(self.request, context)
        return context

class GerenciarPedidosView(ListView):
    model = Agendamento
    template_name = 'pedidos_gerenciar.html'

    def get_queryset(self):
        agenda_id = self.kwargs['pk']
        queryset = Agendamento.objects.filter(agenda_id=agenda_id)
        
        for pedido in queryset:
            pedido.hora_fim = pedido.hora_fim.strftime("%H:%M")
            pedido.hora_inicio = pedido.data.time().strftime("%H:%M")
            pedido.dia = pedido.data.date().strftime("%d/%m")
            pedido.dia_semana = DIAS[pedido.data.weekday()][1]

        return queryset
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context = get_menu_data_context(self.request, context)
        agendamentos = Agendamento.objects.filter(agenda__barbearia=self.request.user.barbearia)
        
        context['dia'] = datetime.today().strftime("%d/%m")
        context['dia_semana'] = DIAS[datetime.today().weekday()][1]

        for agendamento in agendamentos:
            print(agendamento.data.date() >= date.today())
            if agendamento.data.date() >= datetime.today().date():
                print(agendamento.data.date())
                context['pedidos'] = agendamento
        context['pedidos'] = None

        
        return context

    def post(self, *args, **kwargs):
        # Processo para aprovar um agendamento
        if is_ajax(self.request):
            pedido_id = self.request.POST.get('pedido_id')
            pedido = get_object_or_404(Agendamento, id=pedido_id)
            pedido.aprovado = True  
            pedido.save()
            return JsonResponse({'message':'Pedido de agendamento aprovado'})
        return JsonResponse({'error':'Requisição inválida'})
            
