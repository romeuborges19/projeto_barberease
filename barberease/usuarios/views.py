from datetime import datetime
from django.contrib import messages
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.signals import pre_social_login
from django.contrib.auth import user_logged_in
from django.contrib.sessions.models import Session
from django.dispatch import receiver
from django.shortcuts import redirect
from django.urls import reverse_lazy
from allauth.account.models import EmailAddress
from barbearia.models import Barbearia
from .models import Usuario
from .forms import UsuarioForm
from allauth.account.views import TemplateView
from barbearia.models import Barbearia
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from allauth.account.signals import user_logged_in
from datetime import datetime, timedelta



def logged_in(sender, **kwargs):
    sociallogin = kwargs['sociallogin']
    email = sociallogin.user.email

    global should_redirect

    if EmailAddress.objects.filter(email=email).exists():
        print("tem email")
        should_redirect = True 
    else:
        print("nao tem email")
        should_redirect = False


pre_social_login.connect(logged_in)

class UsuarioLoginView(LoginView):
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

class ProcessGoogleLoginView(TemplateView):
    template_name = "process_login.html"

    def get(self, request, *args, **kwargs):
        if should_redirect:
            print("caso 1")
            return redirect(reverse_lazy("usuario:home"))
        else:
            print("caso 2")
            usuario = self.request.user

            if usuario.dono_barbearia:
                if Barbearia.objects.filter(dono=usuario).exists():
                    return redirect(reverse_lazy("barbearia:home"))
                else:
                    return redirect(reverse_lazy("barbearia:cadastrar_barbearia"))
            else:
                print("caso 3")
                return redirect(reverse_lazy("usuario:cadastro"))

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

    def get(self, request, *args, **kwargs):
        request.session.flush()
        return super().get(request, *args, **kwargs)
  
