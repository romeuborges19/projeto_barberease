from django.db import models
from barbearia.models import Barbearia, Barbeiros
from usuarios.models import Usuario

MEDIDAS_TEMPO = (
    (1, "Minutos"),
    (2, "Horas"),
)

class Servico(models.Model):
    # Model que armazena os serviços ofertados por cada barbearia.

    nome = models.CharField("Nome do Serviço", max_length=50)
    barbearia = models.ForeignKey(Barbearia, verbose_name="Barbearia", on_delete=models.CASCADE)
    tempo_servico = models.IntegerField("Tempo 'médio' do serviço")
    medida_tempo = models.IntegerField("Medida de Tempo", choices=MEDIDAS_TEMPO)

    def __str__(self):
        return self.nome


class Agenda(models.Model):
    # Model que agrupa os agendamentos de uma barbearia e armazena dados sobre sua lógica de funcionamento.

    horarios_funcionamento= models.JSONField(null=False, blank=True)
    barbearia = models.OneToOneField(Barbearia, verbose_name="Barbeiro", on_delete=models.CASCADE, null=False, blank=True)
    def __str__(self):
        return self.barbearia.nome
    
class Agendamento(models.Model):
    # Model que armazena os dados de um agendamento de serviço de barbearia.

    data = models.DateTimeField()
    hora_fim = models.TimeField(default=None)
    aprovado = models.BooleanField()
    servico = models.ForeignKey(Servico, verbose_name="Servico", on_delete=models.CASCADE)
    agenda = models.ForeignKey(Agenda, verbose_name="Agenda", on_delete=models.CASCADE)
    cliente = models.ForeignKey(Usuario, verbose_name="Cliente", related_name="cliente", on_delete=models.CASCADE)
    barbeiro = models.ForeignKey(Barbeiros, verbose_name="Barbeiro", related_name="barbeiro", null=True, on_delete=models.SET_NULL)
    criado_em = models.DateTimeField(auto_now_add=True)
    modificado_em = models.DateTimeField(auto_now=True)
