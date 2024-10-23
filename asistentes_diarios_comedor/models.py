from django.db import models


class AsistentesDiariosComedor(models.Model):
   
    rango = models.CharField("Rango", max_length=100)
    
    def __str__(self):
        return f"{self.rango}"

    class Meta:
        verbose_name_plural = "Asistentes diarios de los Comedores"


