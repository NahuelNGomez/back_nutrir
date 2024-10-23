from django.contrib import admin
from .models import Provincia
class ProvinciaAdmin(admin.ModelAdmin):
	"""Administrador del modelo Provincia"""
	list_display = ['nombre', 'codigo_UTA']
	ordering = ['nombre']

admin.site.register(Provincia, ProvinciaAdmin)
