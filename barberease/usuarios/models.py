from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    nome = models.CharField("Nome", max_length=150)
    sobrenome = models.CharField("Sobrenome", max_length=150, null=True, blank=True)
    email = models.EmailField("Email", unique=True)
    dono_barbearia= models.BooleanField("Dono da Barbearia", default=False)


    first_name = None
    last_name = None

    def __str__(self):
        return self.nome
    

 
