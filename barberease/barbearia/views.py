from datetime import date, datetime, time
import http
from os import getpid, walk
from typing import Any
from django.core.serializers.json import PythonDeserializer
from django.db import models
from django.shortcuts import HttpResponse, render, redirect
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from agendamento.utils import get_menu_data_context
from usuarios.authentication import create_acess_token, get_acess_token, get_token_user_id
from usuarios.forms import UsuarioForm
from barbearia.forms import BarbeariaForm, BarbeariaUpdateForm, BarbeirosForm
from .models import Barbearia
from agendamento.models import Agenda, Agendamento, Servico 
from usuarios.models import Usuario
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.contrib.auth import login
from barbearia.models import Barbeiros
from django.http import HttpResponse
from django import http
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group as Groups
from django.contrib import messages
import pytz





class CadastrarDonoview(CreateView):
    # Views para renderizar a tela de cadastro de Dono
    
    form_class = UsuarioForm
    model = Usuario
    template_name = "cadastro_dono.html"
    success_url = reverse_lazy("barbearia:cadastrar_barbearia")

    def form_valid(self, form):
        self.object = form.save()
        user = self.object
        user.dono_barbearia = True
        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, user)
        return redirect(self.get_success_url())

class CadastrarBarbeariaview(CreateView):
    # Views para renderizar a tela de cadastro de Barbearia

    model = Barbearia
    form_class = BarbeariaForm
    template_name = "cadastro_barbearia.html"
    
    def form_valid(self, form):
        usuario = Usuario.objects.get(pk=self.request.user.pk)
        form.instance.dono = usuario
        return super().form_valid(form)
    
    def get_success_url(self):
        barbearia = Barbearia.objects.get(dono_id=self.request.user.pk)
        return reverse_lazy("agendamento:cadastrar_agenda")
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("usuarios:login")
        # elif request.user.dono_barbearia:
        #     barbearia_id = Barbearia.objects.filter(dono=request.user).values_list('id', flat=True)
        #     return redirect("barbearia:home", kwargs={'pk':barbearia_id})
        
        return super().dispatch(request, *args, **kwargs)

class HomeBarbeariaView(DetailView):
    # Views para renderizar a tela de home da barbearia
    
    template_name = "home_barbearia.html"
    model = Barbearia

    def get_object(self):
        obj = super().get_object()  
        if obj.dono != self.request.user:
            raise PermissionDenied()
        return obj
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("usuarios:login")
        return super().dispatch(request, *args, **kwargs)
       
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user
        barbearia = usuario.barbearia
        context['usuario'] = usuario
        context['barbearia'] = barbearia
        context['id_agenda'] = barbearia.agenda.id

        agendamentos = Agendamento.objects.filter(agenda__barbearia=barbearia).select_related('cliente', 'servico', 'barbeiro').order_by('data')
        print(agendamentos)
        quantidade_aprovados = agendamentos.filter(aprovado=True).count()
        quantidade_reprovados = agendamentos.filter(aprovado=False).count()

        context['aprovados'] = quantidade_aprovados
        context['pendentes'] = quantidade_reprovados
        context['data_atual'] = date.today()    
    
        for agendamento in agendamentos:
            print(agendamento.data.date())  
            print(date.today())
            if agendamento.aprovado and agendamento.data.date() == date.today():
                print(agendamento)
                context['agendamento'] = agendamento
                break
    
        return context
    
class ProfileBarbeariaView(DetailView):
    # Views para renderizar a tela de perfil da barbearia
    
    model = Barbearia
    template_name = "perfil_barbearia.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        # Carregando dados do usuário
        id_usuario = get_token_user_id(self.request)
        context['usuario'] = self.request.user

        if self.request.user.dono_barbearia:
            barbearia = Barbearia.objects.filter(dono=self.request.user).first()
            context['barbearia'] = barbearia
        else:
            barbearia = Barbearia.objects.filter(id=self.kwargs['pk']).first()
            context['barbearia'] = barbearia

        agenda = Agenda.objects.get(barbearia=self.kwargs['pk'])
        context['id_agenda'] = agenda.pk

        # Verifica se a barbearia está aberta
        now = datetime.now(pytz.timezone('America/Sao_Paulo'))
        now = now.strftime("%H")
        now = now + ':00'

        # Vetor que relaciona o índice da função weekday com o índice de cada dia da semana no banco
        dias = [6, 4, 1, 2, 0, 3, 5]
        hoje = date.today().weekday()
        horarios_hoje = list(agenda.horarios_funcionamento.values())[dias[hoje]]

        if horarios_hoje == []:
            context['aberto'] = "Fechado"
        else:
            for hora in horarios_hoje:
                if hora == now:
                    context['aberto'] = "Aberto agora"
                    break
            context['fecha_as'] = horarios_hoje[0].strip(":00")

        return context
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("usuarios:login")
        return super().dispatch(request, *args, **kwargs)
    
    # def get_object(self):
    #     obj = super().get_object()
    #     if obj.dono != self.request.user:
    #         raise PermissionDenied()
    #     return obj


class EditarBarbeariaView(UpdateView):
    # Views para renderizar a tela de edição da barbearia
    
    model = Barbearia
    form_class = BarbeariaUpdateForm
    template_name = "editar_barbearia.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context = get_menu_data_context(self.request, context)

        return context

    def get_success_url(self):
        id_barbearia = self.kwargs['pk']
        return reverse_lazy("barbearia:perfil_barbearia", kwargs={'pk':id_barbearia})

    def form_valid(self, form):
        user = self.request.user
        form.instance.dono = user
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("usuarios:login")
        return super().dispatch(request, *args, **kwargs)
    
    def get_object(self):
        obj = super().get_object()
        if obj.dono != self.request.user:
            raise PermissionDenied()
        return obj
    

class CadastrarBarbeirosView(CreateView):
    # Views para renderizar a tela de cadastro de barbeiros
    
    model = Barbeiros 
    form_class = BarbeirosForm
    template_name = "cadastrar_barbeiros.html"
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_menu_data_context(self.request, context)
        
        return context

    def form_valid(self, form):
        user = self.request.user
        barbearia = Barbearia.objects.filter(dono=user).first()
        form.instance.barbearia = barbearia
        messages.success(self.request, 'Barbeiro cadastrado com sucesso!')  
        return super().form_valid(form)
    
    def get_success_url(self):
        user = self.request.user
        barbearia = Barbearia.objects.filter(dono=user).first()
        return reverse_lazy("barbearia:listar_barbeiros")
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("usuarios:login")
        elif not request.user.dono_barbearia:
            return http.HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

class ListarBarbeiros(ListView):
    # Views para renderizar a tela de listagem de barbeiros
    
    model = Barbeiros
    template_name = 'barbeiros_listagem.html'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_menu_data_context(self.request, context)


        return context
        
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("usuarios:login")
        return super().dispatch(request, *args, **kwargs)


class DeletarBarbeiros(DeleteView):
    # Views para renderizar a tela de deletar barbeiros
    
    model = Barbeiros
    success_url = reverse_lazy("barbearia:listar_barbeiros")
    template_name = 'barbeiros_deletar.html'
    context_object_name = 'barbeiro'
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        user = self.request.user
        barbearia = Barbearia.objects.filter(dono=user).first()
        
        if not request.user.is_authenticated:
            return redirect("usuarios:login")
        elif obj.barbearia_id != barbearia.id:
                raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_menu_data_context(self.request, context)

        return context


class EditarBarbeirosView(UpdateView):
    # Views para renderizar a tela de edição de barbeiros
    
    model = Barbeiros
    form_class = BarbeirosForm
    template_name = "barbeiros_editar.html"
    success_url = reverse_lazy("barbearia:listar_barbeiros")
    context_object_name = 'barbeiro'

    def form_valid(self, form):
        user = self.request.user
        barbearia = Barbearia.objects.filter(dono=user).first()
        form.instance.barbearia = barbearia

        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        user = self.request.user
        barbearia = Barbearia.objects.filter(dono=user).first()
        
        if not request.user.is_authenticated:
            return redirect("usuarios:login")
        elif obj.barbearia_id != barbearia.id:
                raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_menu_data_context(self.request, context) 
        
        return context
    
