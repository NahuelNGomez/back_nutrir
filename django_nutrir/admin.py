from pprint import pprint
from django.contrib import admin
from .diccionarios.diccionario_responsable_organizacion import diccionario_responsable_organizacion
from .diccionarios.diccionario_administrador import diccionario_administrador
from .diccionarios.diccionario_superusuario import diccionario_superusuario


def get_app_list(self, request, app_label=None):
	"""
	Return a sorted list of all the installed apps that have been
	registered in this site.
	"""

	#app_dict = self._build_app_dict(request, app_label)
	#pprint(app_dict)

	usuario = request.user

	if usuario.is_superuser:
		if app_label == 'comedor':
			return [diccionario_superusuario[0]]
		elif app_label == 'comida':
			return [diccionario_superusuario[1]]
		elif app_label == 'actividad_complementaria_comedor':
			return [diccionario_superusuario[2]]
		elif app_label == 'encuesta':
			return [diccionario_superusuario[3]]
		elif app_label == 'departamento':
			return [diccionario_superusuario[4]]
		elif app_label == 'admin_interface':
			return [diccionario_superusuario[5]]
		elif app_label == 'organizacion':
			return [diccionario_superusuario[6]]
		elif app_label == 'reporte':
			return [diccionario_superusuario[7]]
		elif app_label == 'sites':
			return [diccionario_superusuario[8]]
		elif app_label == 'account':
			return [diccionario_superusuario[9]]
	elif usuario.groups.filter(name='Administrador').exists():
		if app_label == 'comedor':
			return [diccionario_administrador[0]]
		elif app_label == 'comida':
			return [diccionario_administrador[1]]
		elif app_label == 'actividad_complementaria_comedor':
			return [diccionario_administrador[2]]
		elif app_label == 'encuesta':
			return [diccionario_administrador[3]]
		elif app_label == 'departamento':
			return [diccionario_administrador[4]]
		elif app_label == 'organizacion':
			return [diccionario_administrador[5]]
		elif app_label == 'reporte':
			return [diccionario_administrador[6]]
		elif app_label == 'account':
			return [diccionario_superusuario[7]]
	elif usuario.groups.filter(name='Responsable Organizacion').exists():
		if app_label == 'comedor':
			return [diccionario_responsable_organizacion[0]]
		elif app_label == 'comida':
			return [diccionario_responsable_organizacion[1]]
		elif app_label == 'encuesta':
			return [diccionario_responsable_organizacion[2]]
		elif app_label == 'organizacion':
			return [diccionario_responsable_organizacion[3]]
		elif app_label == 'reporte':
			return [diccionario_responsable_organizacion[4]]

	if usuario.is_superuser:
		return diccionario_superusuario
	elif usuario.groups.filter(name='Administrador').exists():
		return diccionario_administrador
	elif usuario.groups.filter(name='Responsable Organizacion').exists():
		return diccionario_responsable_organizacion

admin.AdminSite.get_app_list = get_app_list
