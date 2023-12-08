from django.test import TestCase
from django.urls import reverse, resolve

class TestViews(TestCase):
    
    def test_home_GET(self):
        response = self.client.get(reverse('usuario:home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuario_home.html')
