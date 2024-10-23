from django.db import models

class Provincia(models.Model):
    """  Modelo para representar las provincias que figuran en
    las Unidades Territoriales del sitio de Obras Públicas """
    nombre = models.CharField("Nombre", max_length=100)
    codigo_UTA = models.CharField( "Codigo UTA", unique=True, max_length=20)

    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        verbose_name_plural = "Provincias"
