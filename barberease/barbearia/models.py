from django.db import models
from usuarios.models import Usuario
from django.db.models.signals import pre_save

class Barbearia(models.Model):
    
    nome = models.CharField("Nome", max_length=150)
    cnpj = models.CharField("CNPJ", max_length=14, unique=True, default=None)
    endereco = models.CharField("Endereço", max_length=150)
    telefone = models.CharField("Telefone", max_length=150)
    cep = models.CharField("CEP", max_length=9)
    setor = models.CharField("Setor", max_length=150)
    cidade = models.CharField("Cidade", max_length=150)
    estado = models.CharField("Estado", max_length=150)
    dono = models.OneToOneField(Usuario, verbose_name="Dono", on_delete=models.CASCADE, unique=True, null=True)
    complemento = models.CharField("Complemento", max_length=150, null=True, blank=True)    
    logo = models.ImageField("Logo", upload_to="images", null=True, blank=True)

    class Meta:
        verbose_name = "Barbearia"
        verbose_name_plural = "Barbearias"
        unique_together = ('cnpj', 'dono')

    def __str__(self):
        return self.nome
    
class Barbeiros(models.Model):

    nome = models.CharField("Nome", max_length=150)
    email = models.EmailField("Email", max_length=150, unique=True, default=None, null=True)
    barbearia = models.ForeignKey(Barbearia, verbose_name="Barbearia", on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


