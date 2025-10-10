from email.policy import default
from typing_extensions import Required
from django.db import models

from enum import Enum


class Unidad(models.Model):
    nombre = models.CharField(max_length=10, unique=True)
    equivalencia_gramos = models.DecimalField("Equivalencia en gramos", null=True, blank=True, decimal_places=2, max_digits=16, help_text="Equivalencia de 1 unidad en gramos")
    equivalencia_ml = models.DecimalField("Equivalencia en ml", null=True, blank=True, decimal_places=2, max_digits=16, help_text="Equivalencia de 1 unidad en ml")
    
    def clean(self):
        from django.core.exceptions import ValidationError
        # Validar que solo se puede llenar uno de los dos campos
        if self.equivalencia_gramos and self.equivalencia_ml:
            raise ValidationError("No se puede especificar equivalencia en gramos y ml al mismo tiempo.")
        if not self.equivalencia_gramos and not self.equivalencia_ml:
            raise ValidationError("Debe especificar equivalencia en gramos o ml.")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        if self.equivalencia_gramos:
            return f"{self.nombre} ({self.equivalencia_gramos}g)"
        elif self.equivalencia_ml:
            return f"{self.nombre} ({self.equivalencia_ml}ml)"
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Unidades"

class Alimento(models.Model):
    nombre = models.CharField("Nombre", max_length=100, unique=True)
    foto = models.ImageField(upload_to='images')
    cantidad_porcion = models.DecimalField("Cantidad de Referencia", null=False, blank=False, decimal_places=2, max_digits=16)
    unidades = models.ManyToManyField(Unidad, verbose_name="Unidades utilizables")
    
    # Nutrientes básicos
    agua = models.DecimalField("Agua", null=False, blank=False, decimal_places=2, max_digits=16, help_text="En gramos", default=0)
    energia = models.DecimalField("Kilocalorias", null=False, blank=False, decimal_places=2, max_digits=16, default=0)
    proteinas = models.DecimalField("Proteinas", null=False, blank=False, decimal_places=2, max_digits=16, help_text="En gramos", default=0)
    lipidos = models.DecimalField("Lípidos", null=False, blank=False, decimal_places=2, max_digits=16, help_text="En gramos", default=0)
    
    # Ácidos grasos
    acidos_grasos_saturados = models.DecimalField("Ácidos Grasos Saturados", null=False, blank=False, decimal_places=2, max_digits=16, help_text="En gramos", default=0)
    acidos_grasos_monoinsaturados = models.DecimalField("Ácidos Grasos Monoinsaturados", null=False, blank=False, decimal_places=2, max_digits=16, help_text="En gramos", default=0)
    acidos_grasos_poliinsaturados = models.DecimalField("Ácidos Grasos Poliinsaturados", null=False, blank=False, decimal_places=2, max_digits=16, help_text="En gramos", default=0)
    colesterol = models.DecimalField("Colesterol", null=False, blank=False, decimal_places=2, max_digits=16, help_text="En mg", default=0)
    
    # Carbohidratos y fibra
    hidratos_carbono = models.DecimalField("Hidratos de Carbono", null=False, blank=False, decimal_places=2, max_digits=16, help_text="En gramos", default=0)
    fibra = models.DecimalField("Fibra", null=False, blank=False, decimal_places=2, max_digits=16, help_text="En gramos", default=0)
    cenizas = models.DecimalField("Cenizas", null=False, blank=False, decimal_places=2, max_digits=16, help_text="En gramos", default=0)
    
    # Minerales
    sodio = models.DecimalField("Sodio", null=False, blank=False, decimal_places=2, max_digits=16, help_text="En mg", default=0)
    potasio = models.DecimalField("Potasio", null=False, blank=False, decimal_places=2, max_digits=16, help_text="En mg", default=0)
    calcio = models.DecimalField("Calcio", null=False, blank=False, decimal_places=2, max_digits=16, help_text="En mg", default=0)
    fosforo = models.DecimalField("Fósforo", null=False, blank=False, decimal_places=2, max_digits=16, help_text="En mg", default=0)
    hierro = models.DecimalField("Hierro", null=False, blank=False, decimal_places=2, max_digits=16, help_text="En mg", default=0)
    zinc = models.DecimalField("Zinc", null=False, blank=False, decimal_places=2, max_digits=16, help_text="En mg", default=0)
    
    # Vitaminas
    niacina = models.DecimalField("Niacina", null=False, blank=False, decimal_places=2, max_digits=16, help_text="En mg", default=0)
    folatos = models.DecimalField("Folatos", null=False, blank=False, decimal_places=2, max_digits=16, help_text="En μg", default=0)
    vitamina_a = models.DecimalField("Vitamina A", null=False, blank=False, decimal_places=2, max_digits=16, help_text="En μg RAE", default=0)
    tiamina = models.DecimalField("Tiamina (B1)", null=False, blank=False, decimal_places=2, max_digits=16, help_text="En mg", default=0)
    riboflavina = models.DecimalField("Riboflavina (B2)", null=False, blank=False, decimal_places=2, max_digits=16, help_text="En mg", default=0)
    vitamina_b12 = models.DecimalField("Vitamina B12", null=False, blank=False, decimal_places=2, max_digits=16, help_text="En μg", default=0)
    vitamina_c = models.DecimalField("Vitamina C", null=False, blank=False, decimal_places=2, max_digits=16, help_text="En mg", default=0)
    vitamina_d = models.DecimalField("Vitamina D", null=False, blank=False, decimal_places=2, max_digits=16, help_text="En UI", default=0)
    
    # Campos legacy para compatibilidad (mantener los nombres antiguos)
    grasas = models.DecimalField("Grasas Saturadas (Legacy)", null=True, blank=True, decimal_places=2, max_digits=16, help_text="En gramos - usar acidos_grasos_saturados")
    grasas_totales = models.DecimalField("Grasas Totales (Legacy)", null=True, blank=True, decimal_places=2, max_digits=16, help_text="En gramos - usar lipidos")

    def __str__(self):
        return f"{self.nombre}"
    
    class Meta:
        verbose_name_plural = "Alimentos"

class AlimentoSARA(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    cantidad_porcion = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    
    # Nutrientes básicos
    agua = models.DecimalField("Agua", max_digits=10, decimal_places=2, default=0, help_text="En gramos")
    energia = models.DecimalField("Energía", max_digits=10, decimal_places=2, default=0, help_text="En kcal")
    proteinas = models.DecimalField("Proteínas", max_digits=10, decimal_places=2, default=0, help_text="En gramos")
    lipidos = models.DecimalField("Lípidos", max_digits=10, decimal_places=2, default=0, help_text="En gramos")
    
    # Ácidos grasos
    acidos_grasos_saturados = models.DecimalField("Ácidos Grasos Saturados", max_digits=10, decimal_places=2, default=0, help_text="En gramos")
    acidos_grasos_monoinsaturados = models.DecimalField("Ácidos Grasos Monoinsaturados", max_digits=10, decimal_places=2, default=0, help_text="En gramos")
    acidos_grasos_poliinsaturados = models.DecimalField("Ácidos Grasos Poliinsaturados", max_digits=10, decimal_places=2, default=0, help_text="En gramos")
    colesterol = models.DecimalField("Colesterol", max_digits=10, decimal_places=2, default=0, help_text="En mg")
    
    # Carbohidratos y fibra
    hidratos_carbono = models.DecimalField("Hidratos de Carbono", max_digits=10, decimal_places=2, default=0, help_text="En gramos")
    fibra = models.DecimalField("Fibra", max_digits=10, decimal_places=2, default=0, help_text="En gramos")
    cenizas = models.DecimalField("Cenizas", max_digits=10, decimal_places=2, default=0, help_text="En gramos")
    
    # Minerales
    sodio = models.DecimalField("Sodio", max_digits=10, decimal_places=2, default=0, help_text="En mg")
    potasio = models.DecimalField("Potasio", max_digits=10, decimal_places=2, default=0, help_text="En mg")
    calcio = models.DecimalField("Calcio", max_digits=10, decimal_places=2, default=0, help_text="En mg")
    fosforo = models.DecimalField("Fósforo", max_digits=10, decimal_places=2, default=0, help_text="En mg")
    hierro = models.DecimalField("Hierro", max_digits=10, decimal_places=2, default=0, help_text="En mg")
    zinc = models.DecimalField("Zinc", max_digits=10, decimal_places=2, default=0, help_text="En mg")
    
    # Vitaminas
    niacina = models.DecimalField("Niacina", max_digits=10, decimal_places=2, default=0, help_text="En mg")
    folatos = models.DecimalField("Folatos", max_digits=10, decimal_places=2, default=0, help_text="En μg")
    vitamina_a = models.DecimalField("Vitamina A", max_digits=10, decimal_places=2, default=0, help_text="En μg RAE")
    tiamina = models.DecimalField("Tiamina (B1)", max_digits=10, decimal_places=2, default=0, help_text="En mg")
    riboflavina = models.DecimalField("Riboflavina (B2)", max_digits=10, decimal_places=2, default=0, help_text="En mg")
    vitamina_b12 = models.DecimalField("Vitamina B12", max_digits=10, decimal_places=2, default=0, help_text="En μg")
    vitamina_c = models.DecimalField("Vitamina C", max_digits=10, decimal_places=2, default=0, help_text="En mg")
    vitamina_d = models.DecimalField("Vitamina D", max_digits=10, decimal_places=2, default=0, help_text="En UI")
    
    # Campos legacy para compatibilidad
    grasas = models.DecimalField("Grasas Saturadas (Legacy)", max_digits=10, decimal_places=2, null=True, blank=True, help_text="En gramos - usar acidos_grasos_saturados")
    grasas_totales = models.DecimalField("Grasas Totales (Legacy)", max_digits=10, decimal_places=2, null=True, blank=True, help_text="En gramos - usar lipidos")

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Alimento SARA"
        verbose_name_plural = "Alimentos SARA"
        ordering = ['nombre']

