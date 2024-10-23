# Generated by Django 4.1.1 on 2022-10-19 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('departamento', '0001_initial'),
        ('provincia', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GobiernoLocal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('tipo_gobierno', models.CharField(max_length=100, verbose_name='Tipo de gobierno')),
                ('codigo_UTA', models.CharField(max_length=20, verbose_name='Codigo UTA')),
                ('latitud', models.CharField(max_length=20, verbose_name='Latitud')),
                ('longitud', models.CharField(max_length=20, verbose_name='Longitud')),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='departamento.departamento')),
                ('provincia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='provincia.provincia')),
            ],
            options={
                'verbose_name_plural': 'Gobiernos Locales',
            },
        ),
    ]
