from allauth.socialaccount.signals import pre_social_login
from django.shortcuts import redirect , render
from django.urls import reverse_lazy
from allauth.account.models import EmailAddress
from barbearia.models import Barbearia
from .models import Usuario
from .forms import UsuarioForm ,UsuarioRedefinePasswordForm, UsuarioNewPasswordForm
from allauth.account.views import TemplateView
from barbearia.models import Barbearia
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView
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
        print(f"global variables:  {globals()}")
        if should_redirect:
            return redirect(reverse_lazy("usuario:home"))
        else:
            usuario = self.request.user

            if usuario.dono_barbearia:
                if Barbearia.objects.filter(dono=usuario).exists():
                    return redirect(reverse_lazy("barbearia:home"))
                else:
                    return redirect(reverse_lazy("barbearia:cadastrar_barbearia"))
            else:
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['barbearias'] = Barbearia.objects.all()
        return context
 
class UsuarioLogoutView(LogoutView):
    # Views para renderizar a tela inicial Cliente

    template_name = "registration/login.html"

    def get(self, request, *args, **kwargs):
        request.session.flush()
        return super().get(request, *args, **kwargs)
  
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
                 return render(request, "usuario_redefinir_senha.html" ,{'mensagem': "Siga as instruções no seu e-mail  para redefinir sua senha."})
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
            raise Http404("Nenhum registro de usuário correspondente ao email encontrado.")
                
        if token:
            if token_generator_password.check_token(user,token ) == False:
                return render(request, "usuario_new_password.html",{"mensagem": "Sessão expirada , envie outro email para redefinir senha "})            
                
        else :
            raise Http404("Nenhum registro correspondente ao token encontrado")
        
        if form.is_valid() and user is not None:
                # Os campos foram validados com sucesso
                form.save(user)
                if 'email_para_redefinicao' in request.session:
                    del request.session['email_para_redefinicao']
                
                
                return render(request, "usuario_new_password.html", {'mensagemLoginSucesso': 'Senha redefinida com sucesso. Faça o login com sua nova senha.'})
                
        
        return render(request, "usuario_new_password.html", {'form': form})