# Generated by Django 4.2.1 on 2023-10-10 10:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("usuarios", "0002_alter_usuario_sobrenome"),
    ]

    operations = [
        migrations.AddField(
            model_name="usuario",
            name="logo",
            field=models.ImageField(
                blank=True, null=True, upload_to="images", verbose_name="Logo"
            ),
        ),
    ]
