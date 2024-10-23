from django.db import models
from provincia.models import Provincia
from departamento.models import Departamento

class GobiernoLocal(models.Model):
    """  Modelo para representar los gobiernos locales que figuran en
    las Unidades Territoriales del sitio de Obras Públicas """
    nombre = models.CharField("Nombre", max_length=100)
    tipo_gobierno = models.CharField("Tipo de gobierno", max_length=100)
    codigo_UTA = models.CharField( "Codigo UTA", max_length=20)
    departamento = models.ForeignKey(Departamento, models.CASCADE)
    provincia = models.ForeignKey(Provincia, models.CASCADE)
    latitud = models.CharField("Latitud", max_length=20)
    longitud = models.CharField("Longitud", max_length=20)
    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        verbose_name_plural = "Gobiernos Locales"

