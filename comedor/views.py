from django.contrib.postgres.aggregates import StringAgg, ArrayAgg
from django.db.models import Sum, Value
from django.db.models.functions import Concat
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import ComedorSerializer, FuncionamientoComedorSerializer, \
	FuncionamientoComedorSerializerPost  # , OtrasActividadesComedorSerializer
from .models import Comedor, FuncionamientoComedor  # , OtrasActividadesComedor

# VISTA PARA CAMPOS ANIDADOS (PROVINCIA, DEPARTAMENTO,GOBIERNO LOCAL, LOCALIDAD)

from dal import autocomplete
from provincia.models import Provincia
from departamento.models import Departamento
from gobierno_local.models import GobiernoLocal
from localidad.models import Localidad

import django_filters
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class ProvinciaAutoComplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		# Don't forget to filter out results depending on the visitor !
		if not self.request.user.is_authenticated:
			return Provincia.objects.none()
		qs = Provincia.objects.all().order_by('nombre')
		if self.q:  # para que en el listado se pueda buscar por nombre de la provincia
			qs = qs.filter(nombre__istartswith=self.q)
		return qs


class DepartamentoAutoComplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		# Don't forget to filter out results depending on the visitor !
		if not self.request.user.is_authenticated:
			return Departamento.objects.none()

		provincia = self.forwarded.get('provincia', None)
		if provincia is not None:
			qs = Departamento.objects.filter(provincia=provincia).order_by('nombre')
			if self.q:  # para que en el listado se pueda buscar por nombre de la provincia
				qs = qs.filter(nombre__istartswith=self.q)
		else:
			qs = Departamento.objects.none()
		return qs


class GobiernoLocalAutoComplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		# Don't forget to filter out results depending on the visitor !
		if not self.request.user.is_authenticated:
			return GobiernoLocal.objects.none()

		departamento = self.forwarded.get('departamento', None)
		if departamento is not None:
			qs = GobiernoLocal.objects.filter(departamento=departamento).order_by('nombre')
			if self.q:  # para que en el listado se pueda buscar por nombre de la provincia
				qs = qs.filter(nombre__istartswith=self.q)
		else:
			qs = GobiernoLocal.objects.none()
		return qs


class LocalidadAutoComplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		# Don't forget to filter out results depending on the visitor !
		if not self.request.user.is_authenticated:
			return Localidad.objects.none()

		gobiernoLocal = self.forwarded.get('gobierno_local', None)
		if gobiernoLocal is not None:
			# TODO: Unificar filtrado de is_active
			qs = Localidad.objects.filter(gobierno_local=gobiernoLocal).order_by('nombre')
			if self.q:  # para que en el listado se pueda buscar por nombre de la provincia
				qs = qs.filter(nombre__istartswith=self.q)
		else:
			qs = Localidad.objects.none()
		return qs


# Todos los comedores
# Un comedor
# Funcionamiento por comedor
# Otras Actividades por comedor

# Comedores por usuario

class ComedoresViewList(generics.ListAPIView):
	"""Vista para que muestre el listado"""

	serializer_class = ComedorSerializer

	def get_queryset(self):
		return Comedor.objects.all()


class ComedorViewList(generics.ListAPIView, generics.UpdateAPIView):
	"""Vista para que muestre un comedor"""
	serializer_class = ComedorSerializer
	http_method_names = ['get', 'patch']

	def get_queryset(self):
		id = self.kwargs['id']
		return Comedor.objects.filter(id=id)

	def patch(self, request, **kwargs):
		id = self.kwargs['id']
		comedor = Comedor.objects.filter(id=id).first()
		data = {
			'nombre': request.data['nombre'],
			'servicio_comedor': comedor.servicio_comedor,
			'activo': comedor.activo,
			'organizacion_regional': comedor.organizacion_regional,
			'provincia': comedor.provincia,
			'departamento': comedor.departamento,
			'gobierno_local': comedor.gobierno_local,
			'localidad': comedor.localidad,
			'barrio': comedor.barrio,
			'calle': request.data['calle'],
			'numero': request.data['numero'],
			'entre_calles': request.data['entre_calles'],
			'latitud': comedor.latitud,
			'longitud': comedor.longitud,
			'ubicacion_georreferencial': comedor.ubicacion_georreferencial,
			'fecha_inicio_actividad': comedor.fecha_inicio_actividad,
			'descripcion': comedor.descripcion,
			'actividades': comedor.actividades,
			'cantidad_trabajadores': comedor.cantidad_trabajadores,
			'asistentes_diarios': comedor.asistentes_diarios,
			'tipos_energia': comedor.tipos_energia,
			'fuente_agua': comedor.fuente_agua,
			'fuente_agua_potable': comedor.fuente_agua_potable,
			'responsable_comedor': comedor.responsable_comedor
		}
		serializer = self.get_serializer(instance=comedor, data=data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data)

class FuncionamientoComedorViewList(generics.ListAPIView, generics.UpdateAPIView):
	"""Vista para que muestre el funcionamiento de un comedor"""
	serializer_class = FuncionamientoComedorSerializer
	http_method_names = ['get']

	def list(self, request, *args, **kwargs):
		id = self.kwargs['id']
		funcionamientos_comedor = FuncionamientoComedor.objects.filter(comedor=id).values('id', 'comedor', 'dia', 'funcionamiento')
		funcionamientos_comedor = funcionamientos_comedor.values('dia').annotate(funcionamientos=ArrayAgg('funcionamiento', delimiter=', ', distinct=True)).values('comedor', 'dia', 'funcionamientos')
		return Response({'data': funcionamientos_comedor})


class ComedorUsuarioViewList(generics.ListAPIView):
	"""Vista para ver el listado de comedores que tengo como responsable para gestionar"""
	serializer_class = ComedorSerializer
	http_method_names = ['get']

	# filter_backends = (filters.DjangoFilterBackend,)
	# filterset_class= ConvenioFilter

	def get_queryset(self):
		usuario = self.request.user
		if usuario.groups.filter(name='Responsable Comedor').exists():
			comedores = Comedor.objects.filter(responsable_comedor=usuario).values_list('id', flat=True)
			return Comedor.objects.filter(id__in=comedores)
		else:
			return Comedor.objects.none()

class FuncionamientoPostViewList(generics.ListAPIView):

	serializer_class = FuncionamientoComedorSerializerPost
	http_method_names = ['patch']
	def patch(self, request):
		# Creo la lista de datas
		funcionamientos = []
		for f in request.data['funcionamientos']:
			for i in f['funcionamientos']:
				data = {
					'comedor': request.data['comedor'],
					'dia': f['dia'],
					'funcionamiento': i
				}
				funcionamientos.append(data)
		# Chequeo que todoas los elementos sean validos
		for f in funcionamientos:
			serializer = FuncionamientoComedorSerializer(data=f)
			serializer.is_valid(raise_exception=True)
		# Agrego o borro segun corresponda
		lista = FuncionamientoComedor.objects.filter(comedor=request.data['comedor']).values('id', 'comedor', 'dia', 'funcionamiento')
		for f in funcionamientos:
			i = lista.filter(comedor=f['comedor'], dia=f['dia'], funcionamiento=f['funcionamiento'])
			if not i:
				serializer = FuncionamientoComedorSerializer(data=f)
				serializer.is_valid(raise_exception=True)
				serializer.save()
				lista = lista.exclude(comedor=f['comedor'], dia=f['dia'], funcionamiento=f['funcionamiento'])
			else:
				lista = lista.exclude(id=i.first()['id'])
		for l in lista:
			funcionamiento = FuncionamientoComedor.objects.get(id=l['id'])
			funcionamiento.delete()
		return Response(
                    {"res": "Se actualizaron los funcionamientos del comedor"},
                    status=status.HTTP_200_OK
                )

