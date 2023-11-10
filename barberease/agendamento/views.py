from datetime import datetime, timedelta
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
import time

from agendamento.forms import AgendaForm, AgendamentoForm, ServicoForm
from agendamento.models import Agenda, Agendamento, Servico, Barbeiros
from agendamento.utils import Celula, get_dias_semana, is_ajax, semana_sort
from barbearia.models import Barbearia


# Create your views here.

class RealizarAgendamentoView(CreateView):
    model = Agendamento
    form_class = AgendamentoForm
    template_name = "agendamento_cadastro.html"
    success_url = reverse_lazy("usuario:home")

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
        start = time.time()
        context = super().get_context_data(**kwargs)
        agenda = self.object
        context['agenda'] = agenda 


        # Gerando uma lista que armazena os horários disponíveis da barbearia, 
        # sem repetir valores
        coluna_horarios = []

        agenda.horarios_funcionamento = semana_sort(agenda.horarios_funcionamento.items())

        dias_semana = get_dias_semana()
        context['dias_semana'] = get_dias_semana()
        
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
                    celula.get_agendamentos(self.kwargs['pk'])
                    row.append(celula)
                else: 
                    row.append(Celula(dias_semana[i], hora, False))
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
        context['dias_semana'] = dias_semana 
        
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
                    celula.get_agendamentos(self.kwargs['pk'])
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



# Views de Serviço

class CadastrarServicoView(CreateView):
    model = Servico
    form_class = ServicoForm
    template_name = "servico_cadastro.html"
    success_url = reverse_lazy("agendamento:listar_servicos")

    def form_valid(self, form):
        user = self.request.user
        barbearia = Barbearia.objects.filter(dono=user).first()
        form.instance.barbearia = barbearia
        return super().form_valid(form)

class ListarServicosView(ListView):
    model = Servico
    template_name = 'servicos_listagem.html'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        barbearia = self.request.user.barbearia
        servicos = Servico.objects.filter(barbearia=barbearia).first()
        context['servico'] = servicos
        return context
    
class DeletarServicoView(DeleteView):
    model = Servico
    success_url = reverse_lazy("agendamento:listar_servicos")
    template_name = 'servico_deletar.html'


class GerenciarPedidosView(ListView):
    model = Agendamento
    context_object_name = 'pedidos'
    template_name = 'pedidos_gerenciar.html'

    def get_queryset(self):
        agenda_id = self.kwargs['pk']
        queryset = Agendamento.objects.filter(agenda_id=agenda_id)
        
        return queryset
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['pk'] = self.kwargs['pk']

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
            
