from django.contrib import admin
from .models import TipoOrganizacion

# Register your models here.
class TipoOrganizacionAdmin(admin.ModelAdmin):

    list_display = ['nombre']
    search_fields = ('nombre',)

admin.site.register(TipoOrganizacion, TipoOrganizacionAdmin)