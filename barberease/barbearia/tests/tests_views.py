from django.test import TestCase, Client
from django.urls import reverse
from barbearia.models import Barbearia, Usuario


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.cadastrar_dono_url = reverse('nome_da_app:cadastrar_dono')
        self.cadastrar_barbearia_url = reverse('nome_da_app:cadastrar_barbearia')
        self.home_barbearia_url = reverse('nome_da_app:home_barbearia')
        self.user = Usuario.objects.create_user(username='testuser', password='12345')

    def test_cadastrar_dono_view(self):
        response = self.client.get(self.cadastrar_dono_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastro_dono.html')

    def test_cadastrar_barbearia_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.cadastrar_barbearia_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastro_barbearia.html')

    def test_home_barbearia_view(self):
        response = self.client.get(self.home_barbearia_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home_barbearia.html')
