# Generated by Django 4.2.5 on 2023-09-16 01:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MovieApp', '0013_alter_avatar_user_alter_usuario_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pelicula',
            name='favs',
        ),
    ]
