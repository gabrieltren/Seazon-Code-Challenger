# Generated by Django 3.2.16 on 2023-01-09 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reserva',
            old_name='anucio',
            new_name='anuncio',
        ),
    ]