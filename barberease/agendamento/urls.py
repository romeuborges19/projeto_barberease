from django.urls import path
from .views import *

app_name = "agendamento"

urlpatterns = [
    path("cadastrar/agenda/", CadastrarAgendaView.as_view(), name="cadastrar_agenda"),
]

