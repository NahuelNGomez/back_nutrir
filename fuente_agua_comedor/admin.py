from django.contrib import admin
from .models import FuenteAguaComedor

# Register your models here.
class FuenteAguaComedorAdmin(admin.ModelAdmin):

    list_display = ['nombre']
    search_fields = ('nombre',)

admin.site.register(FuenteAguaComedor, FuenteAguaComedorAdmin)