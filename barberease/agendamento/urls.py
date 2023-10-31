from django.urls import path
from .views import *

app_name = "agendamento"

urlpatterns = [
    path("agenda/<int:pk>", AgendaView.as_view(), name="agenda"),
    path("agenda/cadastrar/", CadastrarAgendaView.as_view(), name="cadastrar_agenda"),
    path("servico/cadastrar/", CadastrarServicoView.as_view(), name="cadastrar_servico"),
    path("realizar/servico/<int:pk>/<slug:dia>/<slug:hora>/", RealizarAgendamentoView.as_view(), name="realizar_agendamento"),
    path("realizar/<int:pk>/", AgendaAgendamentoView.as_view(), name="agenda_agendamento"),
    path("servico", ListarServicosView.as_view(), name="listar_servicos"),
    path("servico/deletar/<int:pk>", DeletarServicoView.as_view(), name="deletar_servicos")
]

