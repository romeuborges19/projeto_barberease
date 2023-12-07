from django import forms
from django.forms.models import HiddenInput
from .models import Agenda, Agendamento, Servico

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
    ("07:00", "07:00"),
    ("08:00", "08:00"),
    ("09:00", "09:00"),
    ("10:00", "10:00"),
    ("11:00", "11:00"),
    ("12:00", "12:00"),
    ("13:00", "13:00"),
    ("14:00", "14:00"),
    ("15:00", "15:00"),
    ("16:00", "16:00"),
    ("17:00", "17:00"),
    ("18:00", "18:00"),
    ("19:00", "19:00"),
    ("20:00", "20:00"),
    ("21:00", "21:00"),
    ("22:00", "22:00"),
)

MINUTOS = (
    ("00", "00"),
    ("05", "05"),
    ("10", "10"),
    ("15", "15"),
    ("20", "20"),
    ("25", "25"),
    ("30", "30"),
    ("35", "35"),
    ("40", "40"),
    ("45", "45"),
    ("50", "50"),
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
            self.fields[f'{dia[0]}'] = forms.MultipleChoiceField(
                choices=HORARIOS,
                widget=forms.CheckboxSelectMultiple,
                required=False,
            )

    def clean(self):
        cleaned_data = super().clean()
        horarios = {}

        for dia in DIAS_SEMANA:
            horarios[f'{dia[0]}'] = cleaned_data.get(f'{dia[0]}', [])
            if not horarios:
                raise forms.ValidationError(f"Selecione pelo menos um horário para {dia[1]}")

        self.cleaned_data['horarios_funcionamento'] = horarios
        return cleaned_data

    def save(self, commit=True):
        instance = super(AgendaForm, self).save(commit=False)
        instance.horarios_funcionamento = self.cleaned_data['horarios_funcionamento']

        if commit:
            instance.save()
        return instance

class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['nome', 'tempo_servico', 'medida_tempo']
    def __init__(self, *args, **kwargs):
        super(ServicoForm, self).__init__(*args, **kwargs)

    def clean(self):
        tempo_servico = self.cleaned_data.get("tempo_servico")  
        medida_tempo = self.cleaned_data.get("medida_tempo")
        nome = self.cleaned_data.get("nome")
        
        if nome:
            if len(nome) < 3 or len(nome) > 50:
                self.add_error('nome', 'Nome inválido')
        if tempo_servico:
            if tempo_servico < 1:
                self.add_error('tempo_servico', 'Tempo inválido: mínimo 1 minuto')
            if tempo_servico > 6 and medida_tempo == 2:
                self.add_error('tempo_servico', 'Tempo inválido: máximo 6 horas')
            elif tempo_servico > 360 and medida_tempo == 1:
                self.add_error('tempo_servico', 'Tempo inválido: máximo 360 minutos')
        if medida_tempo and medida_tempo not in [1, 2]:
            self.add_error('medida_tempo', 'Medida de tempo inválida')
            
        return super().clean()

 

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['servico']

    def __init__(self, *args, **kwargs):
        queryset = kwargs.pop('servico_queryset', None)
        super(AgendamentoForm, self).__init__(*args, **kwargs)

        self.fields['servico'].queryset = queryset
        self.fields['minuto'] = forms.ChoiceField(choices=MINUTOS)

class AprovarAgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['aprovado']

    def __init__(self, *args, **kwargs):
        super(AprovarAgendamentoForm, self).__init__(*args, **kwargs)



