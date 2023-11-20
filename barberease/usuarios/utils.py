from django.urls import reverse_lazy
from barbearia.models import Barbearia
from usuarios.authentication import create_acess_token

def manage_login_redirect(request):
    usuario = request.user

    request.session['id_usuario'] = usuario.id

    if usuario.dono_barbearia:
        request.session['dono'] = True

        barbearia_id = Barbearia.objects.filter(dono_id=usuario.id).values_list('id', flat=True).first()

        if barbearia_id:
            return reverse_lazy("barbearia:home", kwargs={'pk': barbearia_id})
        else:
            return reverse_lazy("barbearia:cadastrar_barbearia")
    else:
        request.session['dono'] = False
        return reverse_lazy("usuario:home")