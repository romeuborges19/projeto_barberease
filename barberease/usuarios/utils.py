from django.urls import reverse_lazy
from barbearia.models import Barbearia

def manage_login_redirect(request):
    usuario = request.user

    request.session['id_usuario'] = usuario.id

    if usuario.dono_barbearia:
        request.session['dono'] = True

        if Barbearia.objects.filter(dono=usuario).exists():
            request.session['barbearia_cadastrada'] = True
            return reverse_lazy("barbearia:home")
        else:
            request.session['barbearia_cadastrada'] = False
            return reverse_lazy("barbearia:cadastrar_barbearia")
    else:
        request.session['dono'] = False
        return reverse_lazy("usuario:home")
