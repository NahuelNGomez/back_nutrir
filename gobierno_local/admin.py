from django.contrib import admin
from .models import GobiernoLocal
class GobiernoLocalAdmin(admin.ModelAdmin):
	"""Administrador del modelo Gobeirno Local"""
	list_display = ['nombre','tipo_gobierno', 'codigo_UTA','departamento', 'provincia']
	ordering = ['nombre']
admin.site.register(GobiernoLocal, GobiernoLocalAdmin)
