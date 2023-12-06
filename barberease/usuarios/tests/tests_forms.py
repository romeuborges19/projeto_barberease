from django.test import TestCase
from usuarios.forms import UsuarioForm
from usuarios.models import Usuario

class TestUsuarioForm(TestCase):
    def test_valid_password(self):
        form = UsuarioForm(data={'password': '12345'})
        self.assertTrue(form.is_valid())

    def test_invalid_password(self):
        form = UsuarioForm(data={'password': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('Senha inválida', form.errors['password'])

    def test_valid_password2(self):
        form = UsuarioForm(data={'password2': '12345'})
        self.assertTrue(form.is_valid())
        
    def test_invalid_password(self):
        form = UsuarioForm(data={'password2': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('Senha inválida', form.errors['password2'])

    def test_valid_email(self):
        form = UsuarioForm(email={'email': 'benedito1502@gmail.com'})
        self.assertFalse(form.is_valid())

    def test_invalid_password(self):
        form = UsuarioForm(email={'email': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('E-mail inválido', form.errors['email'])