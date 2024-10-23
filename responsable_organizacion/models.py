from typing_extensions import Required
from django.db import models
from user.models import UsuarioPersonalizado
from organizacion.models import Organizacion


class ResponsableOrganizacion(models.Model):
   
    responsable = models.ForeignKey(UsuarioPersonalizado, models.CASCADE, limit_choices_to={'groups__name': "Responsable Organizacion"})
    #responsable = models.ForeignKey(UsuarioPersonalizado, models.CASCADE)
    organizacion = models.ForeignKey(Organizacion, models.CASCADE)
    

    def __str__(self):
        return f"{self.responsable.cuil}"

    class Meta:
        verbose_name_plural = "Responsables de Organizaciones"