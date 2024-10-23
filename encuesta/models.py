from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings

from comedor.models import Comedor
from comida.models import Comida
from alimento.models import Alimento
from alimento.models import Unidad
from organizacion.models import Organizacion

FUNCIONAMIENTO_CHOICES = (
    ("desayuno", "Desayuno"),
    ("almuerzo", "Almuerzo"),
    ("merienda", "Merienda"),
    ("cena", "Cena"),
    #("olla_popular", "Olla Popular"),
)

class Encuesta(models.Model):

    fecha = models.DateField('Fecha de inicio de actividad', blank=False, null=False)
    comedor = models.ForeignKey(Comedor, models.CASCADE)
    organizacion = models.ForeignKey(Organizacion, models.CASCADE)
    responsable_comedor = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, limit_choices_to={'groups__name': "Responsable Comedor"})
    cantidad_rango_1 = models.IntegerField('Cantidad de Comensales - Rango 1', validators=[MinValueValidator(0)])
    cantidad_rango_2 = models.IntegerField('Cantidad de Comensales - Rango 2', validators=[MinValueValidator(0)])
    cantidad_rango_3 = models.IntegerField('Cantidad de Comensales - Rango 3', validators=[MinValueValidator(0)])
    cantidad_rango_4 = models.IntegerField('Cantidad de Comensales - Rango 4', validators=[MinValueValidator(0)])
    funcionamiento = models.CharField(max_length=30, choices=FUNCIONAMIENTO_CHOICES)


    def __str__(self):
        return f"{self.fecha} - {self.funcionamiento.upper()}"

    class Meta:
        verbose_name_plural = "Encuestas"


class AlimentoEncuesta(models.Model):

	alimento = models.ForeignKey(Alimento, models.CASCADE)
	encuesta = models.ForeignKey(Encuesta, models.CASCADE)
	comida = models.ForeignKey(Comida,  models.CASCADE)
	cantidad = models.DecimalField(decimal_places=3, max_digits=5, validators=[MinValueValidator(0.001)])
	unidad = models.ForeignKey(Unidad, models.CASCADE, default=None)

	def __str__(self):
		return f"{self.alimento.nombre}"

	class Meta:
		verbose_name_plural = "Alimentos de una encuesta"

class NoSeSirvioEncuesta(models.Model):

	fecha = models.DateField()
	comedor = models.ForeignKey(Comedor, models.CASCADE)
	funcionamiento = models.CharField(max_length=30, choices=FUNCIONAMIENTO_CHOICES)

	def __str__(self):
		return f"{str(self.fecha)+' '+str(self.comedor)}"

	class Meta:
		verbose_name_plural = "Encuestas que no se sirvieron"
		unique_together = ('fecha', 'comedor', 'funcionamiento')

