from django.contrib import admin
from .models import CantidadTrabajadoresComedor
from .forms import CantidadTrabajadoresComedorAdminForm
from django.db.models.functions import Cast, Substr
from utils.functions import Position, IntegerField

# Register your models here.
class CantidadTrabajadoresComedorAdmin(admin.ModelAdmin):

    list_display = ['rango']
    search_fields = ('rango',)
    form = CantidadTrabajadoresComedorAdminForm
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        posicion_guion = Position('rango', expression="'-'")

        return qs.annotate(
            valor_inicial=Cast(Substr('rango', 1, posicion_guion-1), IntegerField())
        ).order_by('valor_inicial')

admin.site.register(CantidadTrabajadoresComedor, CantidadTrabajadoresComedorAdmin)