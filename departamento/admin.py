from django.contrib import admin
from .models import Departamento

class DepartamentoAdmin(admin.ModelAdmin):
	"""Administrador del modelo Departamento"""
	list_display = ['nombre', 'codigo_UTA', 'provincia']
	ordering = ['nombre']

admin.site.register(Departamento, DepartamentoAdmin)
