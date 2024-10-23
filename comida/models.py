from email.policy import default
from typing_extensions import Required
from django.db import models
from alimento.models import Alimento


HORARIO_CHOICES = (
    ("desayuno_merienda_bebidas", "Desayuno/Merienda - Bebidas"),
    ("desayuno_merienda_comida", "Desayuno/Merienda - Comida"),
    ("almuerzo_cena_entrada", "Almuerzo/Cena - Entrada"),
    ("almuerzo_cena_plato_principal", "Almuerzo/Cena - Plato Principal"),
    ("almuerzo_cena_postre", "Almuerzo/Cena - Postre"),
)


class Comida(models.Model):

    nombre = models.CharField("Nombre", max_length=100, unique=True)
    foto = models.ImageField(upload_to='images', null=False, blank=False)
    alimento = models.ManyToManyField(Alimento, blank=True)
    horario = models.CharField('Horario a servir', max_length=50, choices=HORARIO_CHOICES)
    #cantidad_porcion = models.DecimalField("Cantidad porción (en gramos)", null=False, blank=False, decimal_places=2, max_digits=16)
    #hidratos_carbono = models.DecimalField("Hidratos de Carbono (en gramos)", null=False, blank=False, decimal_places=2, max_digits=16)
    #proteinas = models.DecimalField("Proteinas (en gramos)", null=False, blank=False, decimal_places=2, max_digits=16)
    #grasas = models.DecimalField("Grasas (en gramos)", null=False, blank=False, decimal_places=2, max_digits=16)
    #energia = models.DecimalField("Energia (kilocalorias)", null=False, blank=False, decimal_places=2, max_digits=16)


    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        verbose_name_plural = "Comidas"
