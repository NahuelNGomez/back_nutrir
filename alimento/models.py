from email.policy import default
from typing_extensions import Required
from django.db import models

from enum import Enum


class Unidad(models.Model):
    nombre = models.CharField(max_length=10, unique=True)
    def __str__(self):
        return self.nombre
    class Meta:
        verbose_name_plural = "Unidades"

class Alimento(models.Model):
    nombre = models.CharField("Nombre", max_length=100, unique=True)
    foto = models.ImageField(upload_to='images')
    cantidad_porcion = models.DecimalField("Cantidad de Referencia", null=False, blank=False, decimal_places=2, max_digits=16)
    unidades = models.ManyToManyField(Unidad, verbose_name="Unidades utilizables")
    hidratos_carbono = models.DecimalField("Hidratos de Carbono", null=False, blank=False, decimal_places=2, max_digits=16, help_text="En gramos")
    proteinas = models.DecimalField("Proteinas", null=False, blank=False, decimal_places=2, max_digits=16, help_text="En gramos")
    grasas = models.DecimalField("Grasas Saturadas", null=False, blank=False, decimal_places=2, max_digits=16, help_text="En gramos")
    grasas_totales = models.DecimalField("Grasas Totales", null=False, blank=False, decimal_places=2, max_digits=16, help_text="En gramos")
    energia = models.DecimalField("Kilocalorias", null=False, blank=False, decimal_places=2, max_digits=16)
    sodio = models.DecimalField("Sodio", null=False, blank=False, decimal_places=2, max_digits=16, help_text="En gramos")

    def __str__(self):
        return f"{self.nombre}"
    
    class Meta:
        verbose_name_plural = "Alimentos"

class AlimentoSARA(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    cantidad_porcion = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    hidratos_carbono = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    proteinas = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grasas = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grasas_totales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    energia = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sodio = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.nombre

