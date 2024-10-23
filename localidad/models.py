from django.db import models
from provincia.models import Provincia
from departamento.models import Departamento
from gobierno_local.models import GobiernoLocal

# Create your models here.
class Localidad(models.Model):
    """  Modelo para representar las localidades que figuran en
    las Unidades Territoriales del sitio de Obras Públicas """
    nombre = models.CharField("Nombre", max_length=100)
    codigo_UTA = models.CharField( "Codigo UTA", max_length=20)
    gobierno_local = models.ForeignKey(GobiernoLocal, models.CASCADE)
    departamento = models.ForeignKey(Departamento, models.CASCADE)
    provincia = models.ForeignKey(Provincia, models.CASCADE)
    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        verbose_name_plural = "Localidades"

