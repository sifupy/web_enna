# Generated by Django 5.0.4 on 2024-05-01 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matricule', models.CharField(max_length=20, unique=True)),
                ('mot_de_passe', models.CharField(max_length=128)),
                ('is_admin', models.BooleanField(default=False)),
            ],
        ),
    ]
