from django.db import models


class Genero(models.Model):
   
    nombre = models.CharField("Nombre", max_length=100)
    
    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        verbose_name_plural = "Géneros"


