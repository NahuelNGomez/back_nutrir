from django.db import models


class ServicioComedor(models.Model):
   
    nombre = models.CharField("Nombre", max_length=100)
    
    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        verbose_name_plural = "Servicios Comedores"


