from django.dispatch import receiver
from .models import Barbearia
import datetime
import os
from django.db.models.signals import pre_save

@receiver(pre_save, sender=Barbearia)
def hash_image_name(sender, instance, **kwargs):
    if instance.logo:
        data_hora = datetime.datetime.now()
        data_hora = data_hora.strftime("%d-%m-%Y_%H-%M-%S")
        # getting file extension
        ext = os.path.splitext(instance.logo.name)
        instance.logo.name = f"{instance.nome}-{data_hora}{ext}"
        print(instance.logo.name)
    
       
        