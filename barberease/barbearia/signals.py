from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Barbearia
import datetime

@receiver(pre_save, sender=Barbearia)
def hash_image_name(sender, instance, **kwargs):
    if instance.logo:
        data_hora = datetime.datetime.now()
        data_hora = data_hora.strftime("%d-%m-%Y %H-%M-%S").replace(" ", "_")
        instance.logo.name = instance.nome + "-"+data_hora
        print(instance.logo.name)
    
       
        