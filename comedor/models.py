from email.policy import default
from typing_extensions import Required
from django.db import models
from django.conf import settings

from servicio_comedor.models import ServicioComedor
from organizacion.models import Organizacion
from provincia.models import Provincia
from departamento.models import Departamento
from gobierno_local.models import GobiernoLocal
from localidad.models import Localidad
from actividad_complementaria_comedor.models import ActividadComplementariaComedor
from cantidad_trabajadores_comedor.models import CantidadTrabajadoresComedor
from asistentes_diarios_comedor.models import AsistentesDiariosComedor
from tipo_energia_comedor.models import TipoEnergiaComedor
from fuente_agua_comedor.models import FuenteAguaComedor

DAY_CHOICES = (
    ("lunes", "Lunes"),
    ("martes", "Martes"),
    ("miercoles", "Miércoles"),
    ("jueves", "Jueves"),
    ("viernes", "Viernes"),
    ("sabado", "Sábado"),
    ("domingo", "Domingo"),
)

FUNCIONAMIENTO_CHOICES = (
    ("desayuno", "Desayuno"),
    ("almuerzo", "Almuerzo"),
    ("merienda", "Merienda"),
    ("cena", "Cena"),
    #("olla_popular", "Olla Popular"),
)


class Comedor(models.Model):
    #SOLAPA GENERAL
    nombre = models.CharField("Nombre", max_length=100, null=False, blank=False)
    servicio_comedor = models.ForeignKey(ServicioComedor, models.CASCADE, null=True, blank=True)
    activo = models.BooleanField('Activo', default=True)
    organizacion_regional = models.ForeignKey(Organizacion,on_delete=models.CASCADE, null=False, blank=False)
    #SOLAPA UBICACION
    provincia = models.ForeignKey(Provincia, models.CASCADE)
    departamento = models.ForeignKey(Departamento, models.CASCADE, null=True, blank=True)
    gobierno_local = models.ForeignKey(GobiernoLocal, models.CASCADE, null=True, blank=True)
    localidad = models.ForeignKey(Localidad, models.CASCADE, null=True, blank=True)
    barrio = models.CharField("Barrio", max_length=100, null=True, blank=True)
    calle = models.CharField("Calle", max_length=100, null=True, blank=True)
    numero = models.CharField("Número", max_length=15, null=True, blank=True)
    entre_calles = models.CharField("Entre Calles", max_length=200, null=True, blank=True)
    latitud = models.DecimalField("Latitud", max_digits=9, decimal_places=6,  default=0.0, null=True, blank=True)
    longitud = models.DecimalField("Longitud", max_digits=9, decimal_places=6, default=0.0, null=True, blank=True)
    #VER TIPO DE CAMPO
    ubicacion_georreferencial = models.DecimalField("Ubicacion GEO", max_digits=9, decimal_places=6, default=0.0, null=True, blank=True)
    #SOLAPA FUNCIONAMIENTO (TABLA APARTE)
    #SOLAPA ACTIVIDADES
    fecha_inicio_actividad = models.DateField('Fecha de inicio de actividad', null=True, blank=True)
    descripcion = models.CharField('Descripción', max_length=200, null=True, blank=True)
    actividades = models.ManyToManyField(ActividadComplementariaComedor, blank=True)
    #SOLAPA ESPACIO
    cantidad_trabajadores = models.ForeignKey(CantidadTrabajadoresComedor, models.CASCADE, null=True, blank=True)
    asistentes_diarios = models.ForeignKey(AsistentesDiariosComedor, models.CASCADE, null=True, blank=True)
    tipos_energia = models.ForeignKey(TipoEnergiaComedor, models.CASCADE, null=True, blank=True)
    fuente_agua = models.ForeignKey(FuenteAguaComedor, models.CASCADE, null=True, blank=True)
    fuente_agua_potable = models.BooleanField('Fuente de Agua Potable', default=False, null=True, blank=True)
    #SOLAPA USUARIO
    responsable_comedor = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, limit_choices_to={'groups__name': "Responsable Comedor"})


    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        verbose_name_plural = "Comedores"


class FuncionamientoComedor(models.Model):
    comedor = models.ForeignKey(Comedor, models.CASCADE)
    dia = models.CharField(max_length=9,
                  choices=DAY_CHOICES)

    funcionamiento = models.CharField(max_length=30,
                  choices=FUNCIONAMIENTO_CHOICES, blank=True)

    class Meta:
        verbose_name_plural = "Funcionamiento de Comedores"

    def __str__(self):
        return f"{self.funcionamiento}"


