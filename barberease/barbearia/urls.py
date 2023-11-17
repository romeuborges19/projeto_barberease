from django.urls import path
from .views import *

app_name = "barbearia"

#URLs para o app barbearia

urlpatterns = [
    path("<int:pk>", PerfilBarbeariaView.as_view(), name="perfil_barbearia"),
    path("cadastrar/dono", CadastrarDonoview.as_view(), name="cadastrar_dono"),
    path("cadastrar/", CadastrarBarbeariaview.as_view(), name="cadastrar_barbearia"),
    path("home/<int:pk>", HomeBarbeariaView.as_view(), name="home"),
    path("cadastrar/barbeiros", CadastrarBarbeirosView.as_view(), name="cadastrar_barbeiro"),
    path("listar/barbeiros", ListarBarbeiros.as_view(), name="listar_barbeiros"),
    path("deletar/barbeiros/<int:pk>", DeletarBarbeiros.as_view(), name="deletar_barbeiro"),
]
