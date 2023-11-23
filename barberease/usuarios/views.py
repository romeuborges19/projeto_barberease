from allauth.socialaccount.signals import pre_social_login
from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse, redirect, render
from django.urls import reverse_lazy
from allauth.account.models import EmailAddress
from django.views.generic.list import ListView, View
from barbearia.models import Barbearia
from usuarios.authentication import create_acess_token, get_acess_token, get_token_user_id
from .models import Usuario
from .forms import UsuarioForm, UsuarioUpdateForm, UsuarioRedefinePasswordForm, UsuarioNewPasswordForm
from allauth.account.views import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from .utils import manage_login_redirect
from django.utils import timezone
from datetime import datetime
from django.contrib.sessions.models import Session
from django.http import Http404
from .token import token_generator_password
from django.contrib import messages
import time

def logged_in(sender, **kwargs):
    print("logged in")
    sociallogin = kwargs['sociallogin']
    email = sociallogin.user.email

    global should_redirect

    if EmailAddress.objects.filter(email=email).exists():
        print("email existe")
        should_redirect = True 
    else:
        print("email nao existe")
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
        print(f"global variables:  {globals()}")
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
        id = get_token_user_id(self.request)
        usuario = Usuario.objects.filter(pk=id).first()
        print(usuario)
        context['usuario'] = usuario

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

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.instance.id = self.request.user.id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('usuario:perfil', kwargs={'pk': self.kwargs['pk']})
    
# class UsuarioDeleteView(DeleteView):
#     # Views para renderizar a tela de deletar dados do usuario

#     model = Usuario
#     success_url = reverse_lazy("home:listar_servicos")
#     template_name = 'servico_deletar.html'
    
  
class UsuarioRedefinePasswordView(TemplateView):

    template_name = "usuario_redefinir_senha.html"
    
    def post(self, request, *args, **kwargs):
        form = UsuarioRedefinePasswordForm(request.POST)
        
        if 'password_reset_last_attempt' in request.session:
            last_attempt_time = datetime.fromisoformat(request.session['password_reset_last_attempt'])
            time_elapsed = timezone.now() - last_attempt_time

            # Define o intervalo de tempo que o usuário deve aguardar antes de fazer outra solicitação (por exemplo, 1 hora)
            time_limit = timezone.timedelta(minutes = 5)

            if time_elapsed < time_limit:
                time_to_request = time_limit - time_elapsed
                return render(request, "usuario_redefinir_senha.html" ,{'mensagem':f"Aguarde {int(time_to_request.total_seconds() // 60)} minuto(s) e {int(time_to_request.total_seconds() % 60)} segundo(s) para fazer outra solicitação de redefinição de senha."})

        # Atualiza a última tentativa de redefinição de senha na sessão
        request.session['password_reset_last_attempt'] = timezone.now().isoformat()
        
        if form.is_valid():
            
            email = form.cleaned_data.get('email')
            request.session['email_para_redefinicao'] = email
            
            result = form.process_password_reset()

            if result == None :
                 return render(request, "usuario_redefinir_senha.html" ,{'mensagem': "Siga as instruções no seu email  para redefinir sua senha"})
        return render(request, "usuario_redefinir_senha.html", {'form': form})

class UsuarioNewPasswordView(TemplateView):
    template_name = "usuario_new_password.html"
    def post(self, request, *args, **kwargs):
        token = request.GET.get("token")
        user = None
        form = UsuarioNewPasswordForm(request.POST)
        email = None
        
        try:
            email = request.session['email_para_redefinicao']
        except:
            raise Http404("Sessão expirada")
        try:
            user = Usuario.objects.get(email = email)
        except Usuario.DoesNotExist:
            raise Http404("Nenhum registro de usuário correspondente ao email encontrado")
                
        if token:
            if token_generator_password.check_token(user,token ) == False:
                return render(request, "usuario_new_password.html",{"mensagem": "Sessão inspirada , envie outro email para redefinir senha "})            
                
        else :
            raise Http404("Nenhum registro correspondente ao token encontrado")
        
        if form.is_valid() and user is not None:
                # Os campos foram validados com sucesso
                form.save(user)
                if 'email_para_redefinicao' in request.session:
                    del request.session['email_para_redefinicao']
                
                
                return render(request, "usuario_new_password.html", {'mensagemLoginSucesso': 'Senha trocada com sucesso. Faça o login com sua nova senha.'})
                
        
        return render(request, "usuario_new_password.html", {'form': form})
