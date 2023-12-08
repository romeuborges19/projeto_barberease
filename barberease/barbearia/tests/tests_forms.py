from django.test import TestCase
from barbearia.forms import BarbeariaForm
from barbearia.models import Barbearia

class TestBarbeariaForm(TestCase):
    def test_valid_cnpj(self):
        form = BarbeariaForm(data={'cnpj': '12345678901234'})
        self.assertTrue(form.is_valid())

    def test_invalid_cnpj(self):
        form = BarbeariaForm(data={'cnpj': '12345678901'})
        self.assertFalse(form.is_valid())
        self.assertIn('CNPJ inválido', form.errors['cnpj'])

    def test_existing_cnpj(self):
        # Criar uma instância de Barbearia para testar contra um CNPJ existente
        Barbearia.objects.create(cnpj='12345678901234')
        form = BarbeariaForm(data={'cnpj': '12345678901234'})
        self.assertFalse(form.is_valid())
        self.assertIn('CNPJ já cadastrado', form.errors['cnpj'])

    def test_valid_telefone(self):
        form = BarbeariaForm(data={'telefone': '1234567890'})
        self.assertFalse(form.is_valid())
        self.assertIn('Telefone inválido', form.errors['telefone'])

    def test_existing_telefone(self):
        # Criar uma instância de Barbearia para testar contra um telefone existente
        Barbearia.objects.create(telefone='1234567890')
        form = BarbeariaForm(data={'telefone': '1234567890'})
        self.assertFalse(form.is_valid())
        self.assertIn('Telefone já cadastrado', form.errors['telefone'])

    def test_valid_cep(self):
        form = BarbeariaForm(data={'cep': '1234567'})
        self.assertFalse(form.is_valid())
        self.assertIn('CEP inválido', form.errors['cep'])

