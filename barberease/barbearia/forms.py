from logging import raiseExceptions
from usuarios.models import Usuario
from .models import Barbearia
from django import forms
from validate_docbr import CNPJ
from extras.removeMask import remove_mask


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
        self.cleaned_data['cnpj'] = remove_mask(cnpj)
        self.cleaned_data['telefone'] = remove_mask(telefone)
        self.cleaned_data['cep'] = remove_mask(cep)
        usuario = self.usuario

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


        return cleaned_data
