from django.db import models
from provincia.models import Provincia

class Departamento(models.Model):
    """  Modelo para representar los departamentos que figuran en
    las Unidades Territoriales del sitio de Obras Públicas """
    nombre = models.CharField("Nombre", max_length=100)
    codigo_UTA = models.CharField( "Codigo UTA", unique=True, max_length=20)
    provincia = models.ForeignKey(Provincia, models.CASCADE)
    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        verbose_name_plural = "Departamentos"
