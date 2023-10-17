from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .views import ProcessGoogleLoginView, UsuarioLoginView, UsuarioCadastrarView, UsuarioHomeView, UsuarioLogoutView


app_name = "usuario"

#URLs para o app usuario
urlpatterns = [
    path("", UsuarioLoginView.as_view(), name="login"),
    path("cadastrar/", UsuarioCadastrarView.as_view(), name="cadastro"),
    path("home/", UsuarioHomeView.as_view(), name="home"),
    path("logout/", UsuarioLogoutView.as_view(), name="logout"),
    path("process/", ProcessGoogleLoginView.as_view(), name="process"),
]

urlpatterns += staticfiles_urlpatterns()
