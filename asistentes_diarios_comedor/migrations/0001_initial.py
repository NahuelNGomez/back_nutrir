# Generated by Django 4.1.1 on 2022-11-17 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AsistentesDiariosComedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rango', models.CharField(max_length=100, verbose_name='Rango')),
            ],
            options={
                'verbose_name_plural': 'Asistentes diarios de los Comedores',
            },
        ),
    ]
