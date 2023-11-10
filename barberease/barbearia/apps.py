from django.apps import AppConfig

class BarbeariaConfig(AppConfig):
    name = 'barbearia'
    
    def ready(self):
        import barbearia.signals
        
