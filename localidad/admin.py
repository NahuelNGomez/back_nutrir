from django.contrib import admin
from .models import Localidad
class LocalidadAdmin(admin.ModelAdmin):
	"""Administrador del modelo Localidad"""
	list_display = ['nombre','codigo_UTA', 'gobierno_local','departamento', 'provincia']
	ordering = ['nombre']
admin.site.register(Localidad, LocalidadAdmin)
