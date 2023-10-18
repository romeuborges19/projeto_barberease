<<<<<<< HEAD
# Generated by Django 4.2.1 on 2023-10-18 12:40
=======
# Generated by Django 4.2.1 on 2023-10-10 12:28
>>>>>>> 0964f5fe1c6133ca746d72919cd82a347b2d4e85

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Barbearia",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=150, verbose_name="Nome")),
                (
                    "cnpj",
                    models.CharField(
                        default=None, max_length=14, unique=True, verbose_name="CNPJ"
                    ),
                ),
                ("endereco", models.CharField(max_length=150, verbose_name="Endereço")),
                ("telefone", models.CharField(max_length=150, verbose_name="Telefone")),
                ("cep", models.CharField(max_length=9, verbose_name="CEP")),
                ("setor", models.CharField(max_length=150, verbose_name="Setor")),
                ("cidade", models.CharField(max_length=150, verbose_name="Cidade")),
                ("estado", models.CharField(max_length=150, verbose_name="Estado")),
<<<<<<< HEAD
=======
                (
                    "logo",
                    models.ImageField(
                        blank=True, null=True, upload_to="images", verbose_name="Logo"
                    ),
                ),
>>>>>>> 0964f5fe1c6133ca746d72919cd82a347b2d4e85
                (
                    "logo",
                    models.ImageField(
                        blank=True, null=True, upload_to="images", verbose_name="Logo"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Barbeiros",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=150, verbose_name="Nome")),
                (
                    "email",
                    models.EmailField(
                        default=None,
                        max_length=150,
                        null=True,
                        unique=True,
                        verbose_name="Email",
                    ),
                ),
                (
                    "barbearia",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="barbearia.barbearia",
                        verbose_name="Barbearia",
                    ),
                ),
            ],
        ),
    ]
