from django.db import models

from comedor.models import Comedor
from comida.models import Comida
from alimento.models import Alimento
from encuesta.models import Encuesta
from organizacion.models import Organizacion

# Create your models here.
class ReportesGenerales(models.Model):

    class Meta:
        verbose_name_plural = "Reportes generales"

class ReportesRaciones(models.Model):

    class Meta:
        verbose_name_plural = "Reportes de raciones"

class ReporteNutricional(models.Model):

    comedor = models.ForeignKey(Comedor, models.CASCADE)
    organizacion = models.ForeignKey(Organizacion, models.CASCADE)
    encuesta = models.ForeignKey(Encuesta, models.CASCADE)
    fecha = models.DateField()   
    porciones = models.FloatField()
    hidratos = models.FloatField()
    proteinas = models.FloatField()
    grasasSaturadas = models.FloatField()
    grasasTotales = models.FloatField()
    kilocalorias = models.FloatField()
    sodio = models.FloatField()

    def __str__(self):
        fe_str = str(self.fecha)
        return f"{ fe_str + ' ' + self.comedor.nombre + ' ' + self.encuesta.funcionamiento}"

    class Meta:
        verbose_name_plural = "Reportes Nutricional"
