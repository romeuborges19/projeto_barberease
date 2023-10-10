from django.dispatch import receiver
from django.urls import reverse_lazy
from .models import Usuario
from .forms import UsuarioForm
from allauth.account.views import TemplateView
from barbearia.models import Barbearia
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from allauth.socialaccount.signals import pre_social_login
from allauth.socialaccount.models import SocialAccount

class UsuarioLoginView(LoginView):
    # Views para renderizar a tela inicial Usuario

    template_name = "registration/login.html"



    def get_success_url(self):
        usuario = self.request.user
        if usuario.dono_barbearia:
            if Barbearia.objects.filter(dono=usuario).exists():
                return reverse_lazy("barbearia:home")
            else:
                return reverse_lazy("barbearia:cadastrar_barbearia")
        else:
            return reverse_lazy("usuario:home")
        

  

class UsuarioCadastrarView(CreateView):
    # Views para renderizar a tela de cadastro de Cliente

    form_class = UsuarioForm  
    template_name = "usuario_cadastro.html"
    model = Usuario
    success_url = reverse_lazy("usuario:home")

class UsuarioHomeView(TemplateView):
    # Views para renderizar a tela inicial Cliente

    template_name = "usuario_home.html"
 
class UsuarioLogoutView(LogoutView):
    # Views para renderizar a tela inicial Cliente

    template_name = "registration/login.html"
  
