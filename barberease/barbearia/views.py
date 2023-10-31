from django.shortcuts import HttpResponse, render, redirect
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from usuarios.authentication import create_acess_token, get_acess_token
from usuarios.forms import UsuarioForm
from barbearia.forms import BarbeariaForm, BarbeirosForm
from .models import Barbearia
from usuarios.models import Usuario
from django.views.generic.edit import CreateView
from django.contrib.auth import login
from barbearia.models import Barbeiros


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


class CadastrarBarbeirosView(CreateView):
    # Views para renderizar a tela de cadastro de barbeiros
    
    model = Barbeiros 
    form_class = BarbeirosForm
    template_name = "cadastrar_barbeiros.html"
    success_url = reverse_lazy("barbearia:home")
    
    
    