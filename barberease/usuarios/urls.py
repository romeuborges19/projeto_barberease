from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .views import *


app_name = "usuario"

#URLs para o app usuario
urlpatterns = [
    path("", UsuarioLoginView.as_view(), name="login"),
    path("cadastrar/", UsuarioCadastrarView.as_view(), name="cadastro"),
    path("home/", UsuarioHomeView.as_view(), name="home"),
    path("logout/", UsuarioLogoutView.as_view(), name="logout"),
    path("process/", ProcessGoogleLoginView.as_view(), name="process"),
    path("perfil/<int:pk>", UsuarioView.as_view(), name="perfil"),
    path("perfil/editar/<int:pk>", UsuarioAtualizarView.as_view(), name="editar"),
]

urlpatterns += staticfiles_urlpatterns()
