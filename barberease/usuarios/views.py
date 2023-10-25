from allauth.socialaccount.signals import pre_social_login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from allauth.account.models import EmailAddress
from .models import Usuario
from .forms import UsuarioForm
from allauth.account.views import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from .utils import manage_login_redirect

def logged_in(sender, **kwargs):
    sociallogin = kwargs['sociallogin']
    email = sociallogin.user.email

    global should_redirect

    if EmailAddress.objects.filter(email=email).exists():
        should_redirect = True 
    else:
        should_redirect = False

pre_social_login.connect(logged_in)

class UsuarioLoginView(LoginView):
    template_name = "registration/login.html"
    
    def get_success_url(self):
        return manage_login_redirect(self.request) 

class ProcessGoogleLoginView(TemplateView):
    template_name = "process_login.html"

    def get(self, request, *args, **kwargs):
        if should_redirect:
            return redirect(reverse_lazy("usuario:home"))
        else:
            return redirect(manage_login_redirect(self.request)) 

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
  
