from django.db import models
from barbearia.models import Barbearia
from usuarios.models import Usuario

class Servico(models.Model):
    # Model que armazena os serviços ofertados por cada barbearia.

    nome = models.CharField("Nome", max_length=50)
    barbearia = models.ForeignKey(Barbearia, verbose_name="Barbearia", on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)
    modificado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


class Agenda(models.Model):
    # Model que agrupa os agendamentos de uma barbearia e armazena dados sobre sua lógica de funcionamento.

    horarios_disponiveis = models.JSONField()
    barbearia = models.ForeignKey(Barbearia, verbose_name="Barbeiro", on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)
    modificado_em = models.DateTimeField(auto_now=True)


class Agendamento(models.Model):
    # Model que armazena os dados de um agendamento de serviço de barbearia.

    data = models.DateTimeField()
    aprovado = models.BooleanField()
    servico = models.ForeignKey(Servico, verbose_name="Servico", on_delete=models.CASCADE)
    agenda = models.ForeignKey(Agenda, verbose_name="Agenda", on_delete=models.CASCADE)
    cliente = models.ForeignKey(Usuario, verbose_name="Cliente", related_name="cliente", on_delete=models.CASCADE)
    barbeiro = models.ForeignKey(Usuario, verbose_name="Barbeiro", related_name="barbeiro", null=True, on_delete=models.SET_NULL)
    criado_em = models.DateTimeField(auto_now_add=True)
    modificado_em = models.DateTimeField(auto_now=True)
