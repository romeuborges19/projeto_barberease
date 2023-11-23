from .models import Usuario
from django import forms
import re 
from allauth.account.models import EmailAddress
from  .EmitEmail import enviar_email
from .token import token_generator_password
from django.contrib.sessions.models import Session

class UsuarioForm(forms.ModelForm):
    # Formulário para cadastro de usuário
    
    password = forms.CharField(widget=forms.PasswordInput) 
    password2 = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = Usuario
        fields = ['nome', 'sobrenome', 'email', 'password', 'password2']
    
    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        self.fields['password2'].label = 'Confirmação de senha'


    def clean(self):
        cleaned_data = super(UsuarioForm, self).clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        email = cleaned_data.get("email")

        if password and password2 and password == password2:
            if len(password) < 6:
                self.add_error('password', 'A senha deve ter no mínimo 8 caracteres')

            if  re.search('[0-9]', password) is None:
                self.add_error('password', 'A senha deve conter pelo menos um número')

            if re.search('[A-Z]', password) is None:
                self.add_error('password', 'A senha deve conter pelo menos uma letra maiúscula')
        else:
            self.add_error('password2', 'Senhas não conferem')

        if email and Usuario.objects.filter(email=email).exists():
            self.add_error('email', 'E-mail já cadastrado')

        return cleaned_data


    def save(self, commit=True):
        instance = super(UsuarioForm, self).save(commit=False)
        instance.set_password(self.cleaned_data['password'])
        instance.username = self.cleaned_data['email']
        if commit:
            instance.save()
        return instance
    
class UsuarioUpdateForm(forms.ModelForm):
    # Formulário para atualização de usuário
    
    class Meta: 
        model = Usuario
        fields = ['nome', 'sobrenome', 'email']
        
    def clean(self):
        cleaned_data = super(UsuarioUpdateForm, self).clean()
        email = cleaned_data.get("email")
        nome = cleaned_data.get("nome")
        sobrenome = cleaned_data.get("sobrenome")

        if nome:
            if len(nome) < 3:
                self.add_error('nome', 'Nome deve ter no mínimo 3 caracteres')
            elif len(nome) > 100:
                self.add_error('nome', 'Nome deve ter no máximo 50 caracteres')
            elif re.search('[^a-zA-Z]', nome) is not None:
                self.add_error('nome', 'Nome deve conter apenas letras')
                
        if sobrenome:
            if len(sobrenome) < 3:
                self.add_error('sobrenome', 'sobrenome deve ter no mínimo 3 caracteres')
            elif len(sobrenome) > 100:
                self.add_error('sobrenome', 'sobrenome deve ter no máximo 50 caracteres')
            elif re.search('[^a-zA-Z]', sobrenome) is not None:
                self.add_error('sobrenome', 'sobrenome deve conter apenas letras')
        old_email = self.instance.email 
        
        if email:
            if Usuario.objects.filter(email=email).exists():
                self.add_error('email', 'E-mail já cadastrado')
            elif email == old_email:
                self.add_error('email', 'E-mail não pode ser igual ao anterior')

        return cleaned_data
    
    def save(self, commit=True):
        instance = super(UsuarioUpdateForm, self).save(commit=False)
        instance.username = self.cleaned_data['email']
        if commit:
            instance.save()
        return instance


class UsuarioRedefinePasswordForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Digite seu e-mail'}),
        error_messages={
            'invalid': 'Digite um endereço de e-mail válido.',
        }
        
        )
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        
        if EmailAddress.objects.filter(email=email).exists():
            self.add_error('email',"Faça o login pelo Google")

        if email and not Usuario.objects.filter(email=email).exists():
            self.add_error('email', "E-mail não cadastrado")

    def process_password_reset(self ):
        email = self.cleaned_data.get('email')
        usuario = Usuario.objects.get(email=email)
        token = token_generator_password.make_token(usuario)
        enviar_email(token, email)
       
            
class UsuarioNewPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    ConfirmPassword = forms.CharField(widget=forms.PasswordInput)
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        ConfirmPassword = cleaned_data.get('ConfirmPassword')

        if password and ConfirmPassword and password == ConfirmPassword:
            if len(password) < 8:
                self.add_error('password', 'Senha deve ter no mínimo 8 caracteres')

            if not any(char.isdigit() for char in password):
                self.add_error('password', 'Senha deve conter pelo menos um número')

            if not any(char.isupper() for char in password):
                self.add_error('password', 'Senha deve conter pelo menos uma letra maiúscula')
        else:
            self.add_error('ConfirmPassword', 'Senhas não conferem')
            
    def save(self, user):
        user.set_password(self.cleaned_data['password'])
        user.save()
