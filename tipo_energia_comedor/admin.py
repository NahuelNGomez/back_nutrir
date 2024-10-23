from django.contrib import admin
from .models import TipoEnergiaComedor

# Register your models here.
class TipoEnergiaComedorAdmin(admin.ModelAdmin):

    list_display = ['nombre']
    search_fields = ('nombre',)

admin.site.register(TipoEnergiaComedor, TipoEnergiaComedorAdmin)