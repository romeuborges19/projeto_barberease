from django.db import models
from usuarios.models import Usuario
# Create your models here.

class Barbearia(models.Model):
    nome = models.CharField("Nome", max_length=150)
    cnpj = models.CharField("CNPJ", max_length=14, unique=True, default=None)
    endereco = models.CharField("Endereço", max_length=150)
    telefone = models.CharField("Telefone", max_length=150)
    dono = models.ForeignKey(Usuario, verbose_name="Dono", on_delete=models.CASCADE)