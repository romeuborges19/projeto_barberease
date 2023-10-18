from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from usuarios.forms import UsuarioForm
from barbearia.forms import BarbeariaForm
from .models import Barbearia
from usuarios.models import Usuario
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.contrib.auth import login


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

    form_class = BarbeariaForm
    model = Barbearia
    template_name = "cadastro_barbearia.html"

    def form_valid(self, form):
        usuario = Usuario.objects.get(pk=self.request.user.pk)
        form.instance.dono = usuario
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("barbearia:home")
    
class HomeBarbeariaView(TemplateView):
    # Views para renderizar a tela de home da barbearia

    template_name = "home_barbearia.html"
    