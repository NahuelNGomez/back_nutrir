# Generated by Django 4.1.1 on 2022-11-25 18:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('encuesta', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='alimentocomidaencuesta',
            options={'verbose_name_plural': 'Alimentos de una comida de una encuesta'},
        ),
        migrations.AlterModelOptions(
            name='comidaencuesta',
            options={'verbose_name_plural': 'Comidas de una encuesta'},
        ),
        migrations.AlterModelOptions(
            name='encuesta',
            options={'verbose_name_plural': 'Encuestas'},
        ),
    ]
