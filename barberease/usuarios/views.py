from allauth.socialaccount.signals import pre_social_login
from django.shortcuts import HttpResponse, redirect
from django.urls import reverse_lazy
from allauth.account.models import EmailAddress
from django.views.generic.list import ListView, View

from barbearia.models import Barbearia
from usuarios.authentication import create_acess_token, get_acess_token, get_token_user_id
from .models import Usuario
from .forms import UsuarioForm, UsuarioUpdateForm
from allauth.account.views import TemplateView
from django.views.generic.edit import CreateView, UpdateView
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

    def form_valid(self, form):
        response = super().form_valid(form)

        id_usuario = self.request.user.id
        token = create_acess_token(id_usuario)

        response.set_cookie('jwt_token', token, max_age=3600, domain='127.0.0.1')
        response['Location'] = manage_login_redirect(self.request)
        return response

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

class UsuarioHomeView(ListView):
    # Views para renderizar a tela inicial Cliente

    template_name = "usuario_home.html"
    model = Barbearia
    context_object_name = 'usuario'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['id_usuario'] = get_token_user_id(self.request)

        return context 
 
class UsuarioLogoutView(LogoutView):
    # Views para renderizar a tela inicial Cliente

    template_name = "registration/login.html"

    def get(self, request, *args, **kwargs):
        request.session.flush()
        return super().get(request, *args, **kwargs)
  

class UsuarioView(TemplateView):    
    # Views para renderizar o perfil do usuario
    
    template_name = "usuario_perfil.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = get_token_user_id(self.request)
        print(id)
        user =  Usuario.objects.filter(pk=id).first()
        context['usuario'] = Usuario.objects.filter(pk=id).first()
        return context
    

class UsuarioAtualizarView(UpdateView):
    # Views para renderizar a tela de atualizar dados do usuario

    form_class = UsuarioUpdateForm
    template_name = "usuario_atualizar.html"
    model = Usuario
    success_url = reverse_lazy("usuario:perfil")

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.instance.id = self.request.user.id
        return super().form_valid(form)