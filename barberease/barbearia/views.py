from typing import Any
from django.shortcuts import HttpResponse, render, redirect
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from usuarios.authentication import create_acess_token, get_acess_token, get_token_user_id
from usuarios.forms import UsuarioForm
from barbearia.forms import BarbeariaForm, BarbeirosForm
from .models import Barbearia
from agendamento.models import Servico 
from usuarios.models import Usuario
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.contrib.auth import login
from barbearia.models import Barbeiros


class PerfilBarbeariaView(DetailView):
    model = Barbearia
    template_name = "perfil_barbearia.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user

        return context

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
    
class HomeBarbeariaView(DetailView):
    # Views para renderizar a tela de home da barbearia
    
    template_name = "home_barbearia.html"
    model = Barbearia

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        context['barbearia'] = self.request.user.barbearia
        return context
    
class ProfileBarbeariaView(DetailView):
    # Views para renderizar a tela de perfil da barbearia
    
    model = Barbearia
    template_name = "perfil_barbearia.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        id_usuario = get_token_user_id(self.request)
        usuario = Usuario.objects.filter(id=id_usuario).first()
        context['usuario'] = usuario
        barbearia = Barbearia.objects.filter(dono=self.request.user).first()
        context['barbearia'] = barbearia
        return context
    
class CadastrarBarbeirosView(CreateView):
    # Views para renderizar a tela de cadastro de barbeiros
    
    model = Barbeiros 
    form_class = BarbeirosForm
    template_name = "cadastrar_barbeiros.html"

    def form_valid(self, form):
        user = self.request.user
        barbearia = Barbearia.objects.filter(dono=user).first()
        form.instance.barbearia = barbearia
        return super().form_valid(form)

    def get_success_url(self):
        user = self.request.user
        barbearia = Barbearia.objects.filter(dono=user).first()
        return reverse_lazy("barbearia:home", kwargs={'pk':barbearia.id })
    
class ListarBarbeiros(ListView):
    # Views para renderizar a tela de listagem de barbeiros
    
    model = Barbeiros
    template_name = 'barbeiros_listagem.html'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        barbearia = self.request.user.barbearia
        barbeiros = Barbeiros.objects.filter(barbearia=barbearia)
        context['barbeiros'] = barbeiros
        
        return context
 
class DeletarBarbeiros(DeleteView):
    # Views para renderizar a tela de deletar barbeiros
    
    model = Barbeiros
    success_url = reverse_lazy("barbearia:listar_barbeiros")
    template_name = 'barbeiros_deletar.html'
    context_object_name = 'barbeiro'
    
class EditarBarbeirosView(UpdateView):
    # Views para renderizar a tela de edição de barbeiros
    
    model = Barbeiros
    form_class = BarbeirosForm
    template_name = "barbeiros_editar.html"
    success_url = reverse_lazy("barbearia:listar_barbeiros")

    def form_valid(self, form):
        user = self.request.user
        barbearia = Barbearia.objects.filter(dono=user).first()
        form.instance.barbearia = barbearia

        return super().form_valid(form)
