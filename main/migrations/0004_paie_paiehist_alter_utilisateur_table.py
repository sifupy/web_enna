# Generated by Django 5.0.4 on 2024-05-08 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_unite_alter_utilisateur_options_alter_agent_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matag', models.CharField(db_column='MATAG', max_length=5)),
                ('coderub', models.CharField(db_column='CODERUB', max_length=4)),
                ('type', models.CharField(blank=True, db_column='TYPE', max_length=1, null=True)),
                ('libeller', models.CharField(blank=True, db_column='LIBELLER', max_length=150, null=True)),
                ('base', models.DecimalField(blank=True, db_column='BASE', decimal_places=2, max_digits=18, null=True)),
                ('taux', models.FloatField(blank=True, db_column='TAUX', null=True)),
                ('retenues', models.DecimalField(blank=True, db_column='RETENUES', decimal_places=2, max_digits=18, null=True)),
                ('gains', models.DecimalField(blank=True, db_column='GAINS', decimal_places=2, max_digits=18, null=True)),
                ('codeunia', models.CharField(blank=True, db_column='CODEUNIA', max_length=3, null=True)),
            ],
            options={
                'db_table': 'PAIE',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PaieHist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mois', models.CharField(blank=True, db_column='MOIS', max_length=2, null=True)),
                ('exercice', models.CharField(blank=True, db_column='EXERCICE', max_length=4, null=True)),
                ('datep', models.DateTimeField(blank=True, db_column='DATEP', null=True)),
                ('matag', models.CharField(blank=True, db_column='MATAG', max_length=5, null=True)),
                ('coderub', models.CharField(blank=True, db_column='CODERUB', max_length=4, null=True)),
                ('libeller', models.CharField(blank=True, db_column='LIBELLER', max_length=100, null=True)),
                ('base', models.DecimalField(blank=True, db_column='BASE', decimal_places=2, max_digits=18, null=True)),
                ('taux', models.FloatField(blank=True, db_column='TAUX', null=True)),
                ('retenues', models.DecimalField(blank=True, db_column='RETENUES', decimal_places=2, max_digits=18, null=True)),
                ('gains', models.DecimalField(blank=True, db_column='GAINS', decimal_places=2, max_digits=18, null=True)),
                ('type', models.CharField(blank=True, db_column='TYPE', max_length=1, null=True)),
                ('codeunia', models.CharField(blank=True, db_column='CODEUNIA', max_length=3, null=True)),
            ],
            options={
                'db_table': 'PAIE_HIST',
                'managed': False,
            },
        ),
        migrations.AlterModelTable(
            name='utilisateur',
            table='user_pers',
        ),
    ]
