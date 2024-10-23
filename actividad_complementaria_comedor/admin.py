from django.contrib import admin
from .models import ActividadComplementariaComedor

# Register your models here.
class ActividadComplementariaComedorAdmin(admin.ModelAdmin):

    list_display = ['nombre']
    search_fields = ('nombre',)

admin.site.register(ActividadComplementariaComedor, ActividadComplementariaComedorAdmin)