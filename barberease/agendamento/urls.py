from django.urls import path
from .views import *

app_name = "agendamento"

urlpatterns = [
    path("agenda/cadastrar/", CadastrarAgendaView.as_view(), name="cadastrar_agenda"),
    path("agenda/<int:pk>", AgendaView.as_view(), name="agenda"),
]

