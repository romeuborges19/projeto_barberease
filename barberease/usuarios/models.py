from django.db import models
from django.contrib.auth.models import AbstractUser
from allauth.socialaccount.signals import pre_social_login
from allauth.socialaccount.models import SocialAccount , SocialLogin
from django.dispatch import receiver
from django.shortcuts import redirect
from django.urls import reverse_lazy


class Usuario(AbstractUser):
    nome = models.CharField("Nome", max_length=150)
    sobrenome = models.CharField("Sobrenome", max_length=150, null=True, blank=True)
    email = models.EmailField("Email", unique=True)
    dono_barbearia= models.BooleanField("Dono da Barbearia", default=False)
    logo = models.ImageField("Logo", upload_to="images", null=True, blank=True)

    first_name = None
    last_name = None

    def __str__(self):
        return self.nome
    

 
