# Generated by Django 4.2.5 on 2023-09-13 23:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MovieApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pelicula',
            name='portada',
        ),
    ]