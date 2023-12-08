from django.test import TestCase, Client
from django.urls import reverse
from usuarios.models import Usuario

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.process_login_url = reverse('nome_da_app:process_login')
        self.usuario_cadastro_url = reverse('nome_da_app:usuario_cadastro')
        self.usuario_home_url = reverse('nome_da_app:usuario_home')
        self.usuario_new_password_url = reverse('nome_da_app:usuario_new_password')
        self.usuario_redefinhir_senha_url = reverse('nome_da_app:usuario_redefinhir_senha')

    def test_process_login_view(self):
        response = self.client.get(self.process_login_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'process_login.html')

    def test_usuario_cadastro_view(self):
        response = self.client.get(self.usuario_cadastro_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuario_cadastro.html')

    def test_usuario_home_view(self):
        response = self.client.get(self.usuario_home_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuario_home.html')

    def test_usuario_new_password_view(self):
        response = self.client.get(self.usuario_new_password_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuario_new_password.html')

    def test_usuario_redefinhir_senha_view(self):
        response = self.client.get(self.usuario_redefinhir_senha_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuario_redefinhir_senha.html')
