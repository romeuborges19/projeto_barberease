from django.test import TestCase
from usuarios.models import Usuario

class UsuarioTestCase(TestCase):
    def setUp(self):
        Usuario.objects.create(
            nome = "Romeu",
            sobrenome = "Ribeiro",
            email = "romeu22@gmail.com"
            #teste para imagem "Logo"
        )

    def test_retorno_Usuario(self):
        p1 = Usuario.objects.get(nome = 'Romeu')
        self.assetEquals(p1.__str__(), 'Romeu')
        p2 = Usuario.objects.get(sobrenome = 'Ribeiro')
        self.assetEquals(p2.__str__(), 'Ribeiro')
        p3 = Usuario.objects.get(email = 'romeu22@gmail.com')
        self.assetEquals(p3.__str__(), 'romeu22@gmail.com')