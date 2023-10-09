from .models import Usuario
from django import forms
import re 


class UsuarioForm(forms.ModelForm):
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
                self.add_error('password', 'Senha deve ter no mínimo 8 caracteres')

            if  re.search('[0-9]', password) is None:
                self.add_error('password', 'Senha deve conter pelo menos um número')

            if re.search('[A-Z]', password) is None:
                self.add_error('password', 'Senha deve conter pelo menos uma letra maiúscula')
        else:
            self.add_error('password2', 'Senhas não conferem')

        if email and Usuario.objects.filter(email=email).exists():
            self.add_error('email', 'Email já cadastrado')

        return cleaned_data


    def save(self, commit=True):
        instance = super(UsuarioForm, self).save(commit=False)
        instance.set_password(self.cleaned_data['password'])
        instance.username = self.cleaned_data['email']
        print(instance.username)
        if commit:
            print("entrei")
            instance.save()
        return instance
