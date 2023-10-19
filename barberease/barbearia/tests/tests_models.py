from django.test import TestCase
from barbearia.models import Barbearia, Barbeiros

class BarbeariaTestCase(TestCase):
    def setUp(self):
        Barbearia.objects.create(
            nome = "Cortes Ribeiro",
            cnpj = "60074383000174",
            telefone = "6332163777",
            cep = "77016182",
            setor = "Plano Diretor Sul",
            cidade = "Palmas",
            estado = "Tocantins",
            dono = "Marcos Antônio Ribeiro"
        )
    def test_retorno_Barbearia(self):
        p1 = Barbearia.objects.get(nome = 'Cortes Ribeiro')
        self.assetEquals(p1.__str__(), 'Cortes Ribeiro')
        p2 = Barbearia.objects.get(cnpj = '60074383000174')
        self.assetEquals(p2.__str__(), '60074383000174')
        p3 = Barbearia.objects.get(telefone = '6332163777')
        self.assetEquals(p3.__str__(), '6332163777')
        p4 = Barbearia.objects.get(cep = '77016182')
        self.assetEquals(p4.__str__(), '77016182')
        p5 = Barbearia.objects.get(setor = 'Plano Diretor Sul')
        self.assetEquals(p5.__str__(), '77016182')
        p6 = Barbearia.objects.get(cidade = 'Palmas')
        self.assetEquals(p6.__str__(), 'Palmas')
        p7 = Barbearia.objects.get(estado = 'Tocantins')
        self.assetEquals(p7.__str__(), 'Tocantins')
        p8 = Barbearia.objects.get(dono = 'Marcos Antônio Ribeiro')
        self.assetEquals(p8.__str__(), 'Marcos Antônio Ribeiro')

class BarbeirosTestCase(TestCase):
    def setUp(self):
        Barbeiros.objects.create(
            nome = "Benedito Jaime Melo",
            email = "benedito1502@gmail.com"
        )
    def test_retorno_Barbeiros(self):
        p1 = Barbeiros.objects.get(nome = 'Benedito Jaime Melo')
        self.assetEquals(p1.__str__(), 'Benedito Jaime Melo')
        p2 = Barbeiros.objects.get(email = 'benedito1502@gmail.com')
        self.assetEquals(p2.__str__(), 'benedito1502@gmail.com')