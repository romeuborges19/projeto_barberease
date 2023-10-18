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
)

DIAS_SEMANA = (
    ("segunda", "segunda-feira"),
    ("terça", "terça-feira"),
    ("quarta", "quarta-feira"),
    ("quinta", "quinta-feira"),
    ("sexta", "sexta-feira"),
    ("sabado", "sabado"),
    ("domingo", "domingo"),
)

class AgendaForm(forms.ModelForm):
    # Dono preencherá dados que gerarão agenda da barbearia

    def __init__(self, *args, **kwargs):
        super(AgendaForm, self).__init__(*args, **kwargs)

        for dia, label in DIAS_SEMANA:
            self.fields[dia] = forms.MultipleChoiceField(
            choices=HORARIOS_DISPONIVEIS,
            widget=CheckboxSelectMultiple,
            required=True,
            label=label)

    class Meta:
        model = Agenda
        fields = '__all__'
