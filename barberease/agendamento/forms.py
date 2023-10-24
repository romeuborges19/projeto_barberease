from django import forms
from .models import Agenda

DIAS_SEMANA = (
    ("segunda", "segunda-feira"),
    ("terça", "terça-feira"),
    ("quarta", "quarta-feira"),
    ("quinta", "quinta-feira"),
    ("sexta", "sexta-feira"),
    ("sabado", "sabado"),
    ("domingo", "domingo"),
)

HORARIOS = (
    (1, "07:00"),
    (2, "08:00"),
    (3, "09:00"),
    (4, "10:00"),
    (5, "11:00"),
    (6, "12:00"),
    (7, "13:00"),
    (8, "14:00"),
    (9, "15:00"),
    (10, "16:00"),
    (11, "17:00"),
    (12, "18:00"),
    (13, "19:00"),
    (14, "20:00"),
    (15, "21:00"),
    (16, "22:00"),
    (17, "23:00"),
)

class AgendaForm(forms.ModelForm):

    class Meta:
        model = Agenda
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AgendaForm, self).__init__(*args, **kwargs)
        self.fields['barbearia'].widget = forms.HiddenInput()
        self.fields['horarios_funcionamento'].widget = forms.HiddenInput()
        

        for dia in DIAS_SEMANA:
            self.fields[f'horarios_{dia[0]}'] = forms.MultipleChoiceField(
                choices=HORARIOS,
                widget=forms.CheckboxSelectMultiple,
                required=False,
            )

    def clean(self):
        cleaned_data = super().clean()

        for dia in DIAS_SEMANA:
            horarios = cleaned_data.get(f'horarios_{dia[0]}', [])
            if not horarios:
                raise forms.ValidationError(f"Selecione pelo menos um horário para {dia[1]}")

        return cleaned_data










