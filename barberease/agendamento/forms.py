from django.contrib.admin.options import CheckboxSelectMultiple
from .models import *
from django import forms

HORARIOS_DISPONIVEIS = (
    ("1", "5:00"),
    ("2", "6:00"),
    ("3", "7:00"),
    ("4", "8:00"),
    ("5", "9:00"),
    ("6", "10:00"),
    ("7", "11:00"),
    ("8", "12:00"),
    ("9", "13:00"),
    ("10", "14:00"),
    ("11", "15:00"),
    ("12", "16:00"),
    ("13", "17:00"),
    ("14", "18:00"),
    ("15", "19:00"),
    ("16", "20:00"),
    ("17", "21:00"),
    ("18", "22:00"),
    ("19", "23:00"),
    ("20", "Não abrimos"),
)

DIAS_SEMANA = (
    ("semana", "Dias de Semana"),
    ("sabado", "Sábado"),
    ("domingo", "Domingo"),
)

class AgendaForm(forms.ModelForm):
    # Dono preencherá dados que gerarão agenda da barbearia

    class Meta:
        model = Agenda
        exclude = ['horarios_disponiveis', 'barbearia']

    def __init__(self, *args, **kwargs):
        super(AgendaForm, self).__init__(*args, **kwargs)

        for dia, label in DIAS_SEMANA:
            self.fields["horario_entrada_" + dia] = forms.ChoiceField(
            choices=HORARIOS_DISPONIVEIS,
            required=True,
            label=label)


            self.fields["horario_saida_" + dia] = forms.ChoiceField(
            choices=HORARIOS_DISPONIVEIS,
            required=True,
            label=label)

    def clean(self):
        cleaned_data = super(AgendaForm, self).clean()

        entrada_semana = cleaned_data.get("horario_entrada_semana")
        saida_semana = cleaned_data.get("horario_saida_semana")
        entrada_sabado = cleaned_data.get("horario_entrada_sabado")
        saida_sabado = cleaned_data.get("horario_saida_sabado")
        entrada_domingo = cleaned_data.get("horario_entrada_domingo")
        saida_domingo = cleaned_data.get("horario_saida_domingo")

        self.horarios_disponiveis = {"semana": {entrada_semana, saida_semana},
                    "sabado": {entrada_sabado, saida_sabado},
                    "domingo": {entrada_domingo, saida_domingo},
                    }

        return self.horarios_disponiveis
    
    def save(self, commit=True):
        instance = super(AgendaForm, self).save(commit=False)
        instance.horarios_disponiveis = self.horarios_disponiveis

        if commit:
            instance.save()
        return instance
        
