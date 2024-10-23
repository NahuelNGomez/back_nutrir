from email.policy import default
from typing_extensions import Required
from django.db import models
from tipo_organizacion.models import TipoOrganizacion


class Organizacion(models.Model):
   
    nombre = models.CharField("Nombre", max_length=100, unique=True)
    tipo_organizacion = models.ForeignKey(TipoOrganizacion, models.CASCADE)
    logo = models.ImageField(upload_to='images')
    estado = models.BooleanField('Activo', default=False, editable=True)
    es_organizacion_regional = models.BooleanField('Es regional', default=False)    
    organizacion_superior = models.ForeignKey('self',on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        verbose_name_plural = "Organizaciones"