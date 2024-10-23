from django.db import models


class TipoOrganizacion(models.Model):
   
    nombre = models.CharField("Nombre", max_length=100)
    
    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        verbose_name_plural = "Tipo Organizaciones"


