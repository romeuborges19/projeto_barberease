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
        fields = ['nome', 'endereco', 'telefone', 'cnpj']

    def __init__(self, *args, **kwargs):
        super(BarbeariaForm, self).__init__(*args, **kwargs)
        self.fields['cnpj'].widget.attrs['data-mask'] = '00.000.000/0000-00'
        self.fields['telefone'].widget.attrs['data-mask'] = '(00) 00000-0000'

    def clean(self):
        cleaned_data = super(BarbeariaForm, self).clean()
        cnpj = cleaned_data.get("cnpj")
        telefone = self.cleaned_data.get("telefone")
        self.cleaned_data['cnpj'] = remove_mask(cnpj)
        self.cleaned_data['telefone'] = remove_mask(telefone)
        usuario = self.request.user

        if Barbearia.objects.filter(dono=usuario).exists() and usuario.dono_barbearia:
            return raiseExceptions("Você já possui uma barbearia cadastrada com esse usuario")
        
        if cnpj and not validate_cnpj(cnpj):
            self.add_error('cnpj', 'CNPJ inválido')
        

        return cleaned_data