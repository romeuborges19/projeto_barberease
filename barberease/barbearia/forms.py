from logging import raiseExceptions

from django.db.models import Q
from usuarios.models import Usuario
from .models import Barbearia, Barbeiros
from django import forms
from validate_docbr import CNPJ
from extras.removeMask import remove_mask
from usuarios.authentication import get_token_user_id
import os

validate_cnpj = CNPJ()  # validador de cnpj

class BarbeariaForm(forms.ModelForm):

    class Meta:
        model = Barbearia
        fields = ['nome', 'endereco', 'telefone', 'cnpj', 'cep', 'setor', 'cidade', 'estado', 'logo']

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('current_user', None)
        super(BarbeariaForm, self).__init__(*args, **kwargs)
  

    def clean(self):
        cleaned_data = super(BarbeariaForm, self).clean()
        cnpj = cleaned_data.get("cnpj")
        telefone = self.cleaned_data.get("telefone")
        cep = self.cleaned_data.get("cep")  
        logo = self.cleaned_data.get("logo")

        self.cleaned_data['cnpj'] = remove_mask(cnpj)
        self.cleaned_data['telefone'] = remove_mask(telefone)
        self.cleaned_data['cep'] = remove_mask(cep)
        usuario = self.usuario
        tamanho = 5 * 1024 * 1024

        if Barbearia.objects.filter(dono=usuario).exists() and usuario.dono_barbearia:
            return raiseExceptions("Você já possui uma barbearia cadastrada com esse usuario")
        
        if cnpj: 
            if not validate_cnpj.validate(cnpj):
                self.add_error('cnpj', 'CNPJ inválido')

            elif Barbearia.objects.filter(cnpj=cnpj).exists():
                self.add_error('cnpj', 'CNPJ já cadastrado')
        
        if telefone:
            if len(telefone) < 10:
                self.add_error('telefone', 'Telefone inválido')

            elif Barbearia.objects.filter(telefone=telefone).exists():
                self.add_error('telefone', 'Telefone já cadastrado')

        if cep and len(cep) < 8:
            self.add_error('cep', 'CEP inválido')
            
        if logo:
            ext = os.path.splitext(logo.name)
            print(ext)
            if logo.size > tamanho:
                self.add_error('logo', 'Imagem muito grande, tamanho máximo 5MB')
        
            elif ext[1] not in ['.png', '.jpeg', '.jpg']:
                self.add_error('logo', 'Formato de imagem inválido, formatos aceitos: png, jpeg, jpg')
        return cleaned_data

class BarbeariaUpdateForm(forms.ModelForm):
    class Meta:
        model = Barbearia
        fields = ['nome', 'logo', 'descricao', 'telefone', 'cep', 'setor', 'cidade', 'estado', 'complemento']

    def clean(self):
        cleaned_data = super(BarbeariaUpdateForm, self).clean()

        telefone = self.cleaned_data.get("telefone")
        cep = self.cleaned_data.get("cep")
        self.cleaned_data["cep"] = remove_mask(cep)

        logo = self.cleaned_data.get("logo")
        print(f'logo: {logo}')
        tamanho = 5 * 1024 * 1024

        if logo:
            ext = os.path.splitext(logo.name)
            print(ext)
            if logo.size > tamanho:
                self.add_error('logo', 'Imagem muito grande, tamanho máximo 5MB')
        
            elif ext[1] not in ['.png', '.jpeg', '.jpg']:
                self.add_error('logo', 'Formato de imagem inválido, formatos aceitos: png, jpeg, jpg')

        if telefone:
            if len(telefone) < 10:
                self.add_error('telefone', 'Telefone inválido')

            elif Barbearia.objects.filter(~Q(id=self.instance.pk), telefone=telefone).exists():
                self.add_error('telefone', 'Telefone já cadastrado')       

        if cep and len(cep) < 8:
            self.add_error('cep', 'CEP inválido')

        return cleaned_data

    def save(self, commit=True):
        instance = super(BarbeariaUpdateForm, self).save(commit=False)

        if commit:
            instance.save()
        return instance

class BarbeirosForm(forms.ModelForm):
    class Meta:
        model = Barbeiros
        fields = ['nome', 'email']

    def __init__(self, *args, **kwargs):
        self.barbearia = kwargs.pop('barbearia', None)
        super(BarbeirosForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(BarbeirosForm, self).clean()
        email = cleaned_data.get("email")
        nome = cleaned_data.get("nome")
        barbearia = self.barbearia
        if email and Barbeiros.objects.filter(email=email, barbearia=barbearia).exists():
                self.add_error('email', 'Email já cadastrado como barbeiro')
        if nome and len(nome) < 3 or len(nome) > 150:
            self.add_error('nome', 'Nome inválido')
            
        return cleaned_data
