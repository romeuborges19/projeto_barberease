from django.urls import path
from .views import CadastrarDonoview, CadastrarBarbeariaview, HomeBarbeariaView

app_name = "barbearia"

#URLs para o app barbearia

urlpatterns = [
    path("cadastrar/dono/", CadastrarDonoview.as_view(), name="cadastrar_dono"),
    path("cadastrar/", CadastrarBarbeariaview.as_view(), name="cadastrar_barbearia"),
    path("home/<int:pk>", HomeBarbeariaView.as_view(), name="home"),
]
