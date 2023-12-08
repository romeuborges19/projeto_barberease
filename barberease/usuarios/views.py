from typing import Any
from allauth.socialaccount.signals import pre_social_login
from django import http
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import HttpResponse, redirect, render
from django.urls import reverse_lazy
from allauth.account.models import EmailAddress
from django.views.generic.list import ListView, View
from barbearia.models import Barbearia
from usuarios.authentication import create_acess_token, get_acess_token, get_token_user_id
from .models import Usuario
from .forms import UsuarioForm, UsuarioUpdateForm, UsuarioRedefinePasswordForm, UsuarioNewPasswordForm
from allauth.account.views import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView, LogoutView
from .utils import manage_login_redirect
from django.utils import timezone
from datetime import datetime
from django.contrib.sessions.models import Session
from django.http import Http404
from .token import token_generator_password
from django.contrib import messages
import time
from django.contrib.auth.models import Group as Groups
from agendamento.models import Agendamento
from agendamento.utils import get_menu_data_context

def logged_in(sender, **kwargs):
    print("logged in")
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
    
    def form_invalid(self, form):
        messages.error(self.request, "Erro ao fazer login. Verifique suas credenciais.")
        return super().form_invalid(form)

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
    success_url = reverse_lazy("usuario:login")
    
    def form_valid(self, form):
        self.object = form.save()
        user = self.object
        user.save()
        return redirect(self.get_success_url())


class UsuarioHomeView(DetailView):
    # Views para renderizar a tela inicial Cliente

    template_name = "home_usuario.html"
    model = Usuario
    context_object_name = 'usuario'


    # def dispatch(self, request, *args, **kwargs):
    #     usuario_atual = self.get_object()
    #     if request.user.is_authenticated:
    #         if not request.user.dono_barbearia and usuario_atual.id == request.user.id:
    #             return super().dispatch(request, *args, **kwargs)
    #         return http.HttpResponseForbidden()
    #     else:
    #         return redirect(reverse_lazy("usuario:login"))
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = get_token_user_id(self.request)
        usuario = Usuario.objects.filter(pk=id).first()
        context['usuario'] = usuario
        context['barbearias'] = Barbearia.objects.all()
        agendamentos = Agendamento.objects.filter(cliente_id=id, aprovado=True).select_related('agenda__barbearia').order_by('-data')

        agenda_informacao = []
        i = 0
        if agendamentos:
            for agendamento in agendamentos:
                agendamento.hora = agendamento.data.time()
                agendamento.dia = agendamento.data.date()

                if agendamento.aprovado:
                    barbearia = agendamento.agenda.barbearia  
                    agenda_informacao.append({'barbearia': barbearia, 'agendamento': agendamento})
                i+=1
                if(i > 0):
                    break
            context['agendamentos'] = agenda_informacao
        else:
            context['agendamentos'] = False

        return context


class UsuarioLogoutView(LogoutView):
    # Views para renderizar a tela inicial Cliente

    template_name = "registration/login.html"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response = HttpResponseRedirect('/')
        response.delete_cookie('jwt_token', domain='127.0.0.1')
        request.session.flush()

        return response


class UsuarioView(TemplateView):    
    # Views para renderizar o perfil do usuario
    
    template_name = "usuario_perfil.html"
    success_url = '/'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = get_token_user_id(self.request)
        user = Usuario.objects.filter(pk=id).first()
        context['usuario'] = user
        
        if user.dono_barbearia:
            context['barbearia'] = Barbearia.objects.filter(dono_id=id).first()

        return context
    
    def post(self, request, *args, **kwargs):
        
        if request.method == 'POST':
            form = UsuarioRedefinePasswordForm(request.POST)
            id = get_token_user_id(request)
            user = Usuario.objects.filter(pk=id).first()
            context = {
                    'usuario': user,
                    'barbearia': Barbearia.objects.filter(dono_id=id).first() if user.dono_barbearia else None,
                    
                }
                    
            if 'password_reset_last_attempt' in request.session:
                last_attempt_time = datetime.fromisoformat(request.session['password_reset_last_attempt'])
                time_elapsed = timezone.now() - last_attempt_time

                # Define o intervalo de tempo que o usuário deve aguardar antes de fazer outra solicitação (por exemplo, 1 hora)
                time_limit = timezone.timedelta(minutes = 5)

                if time_elapsed < time_limit:
                    time_to_request = time_limit - time_elapsed
                    context['mensagem_time'] = f"Aguarde {int(time_to_request.total_seconds() // 60)} minuto(s) e {int(time_to_request.total_seconds() % 60)} segundo(s) para fazer outra solicitação de redefinição de senha."
                    return render(request, "usuario_perfil.html" ,context)


            if form.is_valid():
                
                result = form.process_password_reset()
                
                if result == None :
                    context['mensagem'] =  "Será enviado um e-mail com instruções para redefinição de senha. O logout será realizado agora."
                    response = super().get(request, *args, **kwargs)
                    response = render(request, "usuario_perfil.html" , context) 
                    response.delete_cookie('jwt_token', domain='127.0.0.1')
                    request.session.flush()
                    
                    # Atualiza a última tentativa de redefinição de senha na sessão
                    request.session['password_reset_last_attempt'] = timezone.now().isoformat()
                    request.session['email_para_redefinicao'] = user.email
                    return response
        
            return render(request, "usuario_perfil.html", {'form': form})


class UsuarioAtualizarView(UpdateView):
    # Views para renderizar a tela de atualizar dados do usuario

    form_class = UsuarioUpdateForm
    template_name = "usuario_atualizar.html"
    model = Usuario

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = get_token_user_id(self.request)
        user =  Usuario.objects.filter(pk=id).first()
        context['usuario'] = user

        if user.dono_barbearia:
            context['barbearia'] = Barbearia.objects.filter(dono_id=id).first()

        return context

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.instance.id = self.request.user.id
        messages.success(self.request, 'Dados atualizados com sucesso!')
        return super().form_valid(form)

    def get_success_url(self):
        print(self)
        return reverse_lazy('usuario:perfil', kwargs={'pk': self.kwargs['pk']})
    
    def dispatch(self, request, *args, **kwargs):
        usuario_atual = self.get_object()
        if request.user.is_authenticated:
            if not request.user.dono_barbearia and usuario_atual.id == request.user.id:
                return super().dispatch(request, *args, **kwargs)
            return http.HttpResponseForbidden()
        else:
            return redirect(reverse_lazy("usuario:login"))
    
    

class UsuarioDeleteView(DeleteView):
    # Views para renderizar a tela de deletar dados do usuario

    model = Usuario
    template_name = "usuario_deletar.html"

    def get_object(self, queryset=None):
        id = get_token_user_id(self.request)
        user = Usuario.objects.filter(pk=id).first()
        return user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        if user.dono_barbearia:
            barbearia = Barbearia.objects.filter(dono_id=user.pk).first()
            if barbearia:
                barbearia.delete()  
        else:
            user.delete()

        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('usuario:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_menu_data_context(self.request, context)
        id = get_token_user_id(self.request)
        user = Usuario.objects.filter(pk=id).first()
        if user.dono_barbearia:
            context['barbearia'] = Barbearia.objects.filter(dono_id=id).first()

        return context
            

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
