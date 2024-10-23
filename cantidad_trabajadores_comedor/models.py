from django.db import models


class CantidadTrabajadoresComedor(models.Model):
   
    rango = models.CharField("Rango", max_length=100)
    
    def __str__(self):
        return f"{self.rango}"

    class Meta:
        verbose_name_plural = "Cantidad de Trabajadores de los Comedores"


