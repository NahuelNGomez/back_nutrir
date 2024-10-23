from django.contrib.postgres.aggregates import ArrayAgg
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import EncuestaSerializer, ComidaEncuestaSerializer, ComidaEncuestaPostSerializer, \
	AlimentoEncuestaCompletoSerializer, NoSeSirvioEncuestaSerializer
from .models import Encuesta, NoSeSirvioEncuesta
from user.models import UsuarioPersonalizado
from comedor.models import Comedor, FuncionamientoComedor
from datetime import date


class EncuestasAdeudadasDiaViewList(generics.ListAPIView):
	"""Vista para devolver las encuestas adeudadas del dia"""
	"""Devuelve: Fecha, Tipo de Comida, Comedor"""

	serializer_class = EncuestaSerializer
	http_method_names = ['get']

	def get(self,request, *args, **kwargs):

		comedor = kwargs['id_c']
		fecha = kwargs['fecha']
		fecha = date(int(fecha[0:4]), int(fecha[5:7]), int(fecha[8:10]))
		usuario = self.request.user.id
		user = UsuarioPersonalizado.objects.get(id=usuario)
		responsable_comedor = user.groups.filter(name='Responsable Comedor').exists()
		if responsable_comedor:
			anio = fecha.year
			mes = fecha.month
			dia = fecha.day
			fecha_actual = date(year=fecha.year, month=mes, day=dia)

			encuestas_dict = {}
			encuestas_records=[]

			#Obtener que dia de la semana es
			#import pdb
			#pdb.set_trace()
			dia_semana = fecha_actual.weekday()
			dias = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']
			dia_semana_txt = dias[dia_semana]

			if FuncionamientoComedor.objects.filter(comedor=comedor,dia=dia_semana_txt).exists():
				funcionamiento_comedor = FuncionamientoComedor.objects.filter(comedor=comedor,dia=dia_semana_txt)
				for funcionamiento in funcionamiento_comedor:
					encuesta = Encuesta.objects.filter(comedor=comedor, fecha=fecha_actual, funcionamiento=funcionamiento.funcionamiento)
					no_se_sirvio = NoSeSirvioEncuesta.objects.filter(comedor=comedor, fecha=fecha_actual, funcionamiento=funcionamiento.funcionamiento)
					if not encuesta and not no_se_sirvio:
						record = {"comedor": comedor, "fecha": str(fecha_actual), "funcionamiento": funcionamiento.funcionamiento}
						encuestas_records.append(record)
			encuestas_dict["encuestas"] = encuestas_records
			return JsonResponse(encuestas_dict,  safe=False)
		else:
			return JsonResponse({'resultado': 'No hay encuestas del día.'}, status=400)




class EncuestasAdeudadasViewList(generics.ListAPIView):
	"""Vista para devolver las encuestas adeudadas del mes en curso"""
	"""Devuelve: Fecha, Tipo de Comida, Comedor"""

	serializer_class = EncuestaSerializer
	http_method_names = ['get']

	def get(self,request, *args, **kwargs):

		comedor = kwargs['id_c']
		fecha = kwargs['fecha']
		import pdb
		#pdb.set_trace()
		fecha = date(int(fecha[0:4]), int(fecha[5:7]), int(fecha[8:10]))
		#fecha = datetime.date.strptime(fecha, "%Y-%m-%d").date()
		usuario = self.request.user.id
		user = UsuarioPersonalizado.objects.get(id=usuario)
		responsable_comedor = user.groups.filter(name='Responsable Comedor').exists()
		if responsable_comedor:
			mes = fecha.month
			dia = fecha.day
			x = range(1, dia+1)

			encuestas_dict = {}
			encuestas_records=[]
			for d in x:
				#recorrer desde el 1 del mes al dia de la fecha parametro
				fecha_actual = date(year=fecha.year, month=mes, day=d)
				#Obtener que dia de la semana es
				dia_semana = fecha_actual.weekday()

				dias = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']
				dia_semana_txt = dias[dia_semana]


				#print(fecha, fecha_actual)

				if FuncionamientoComedor.objects.filter(comedor=comedor, dia=dia_semana_txt).exists():
					funcionamiento_comedor = FuncionamientoComedor.objects.filter(comedor=comedor,dia=dia_semana_txt)
					for funcionamiento in funcionamiento_comedor:
						encuesta = Encuesta.objects.filter(comedor=comedor, fecha=fecha_actual, funcionamiento=funcionamiento.funcionamiento)
						no_se_sirvio = NoSeSirvioEncuesta.objects.filter(comedor=comedor, fecha=fecha_actual, funcionamiento=funcionamiento.funcionamiento)
						if not encuesta and not no_se_sirvio:
							record = {"comedor": comedor, "fecha": str(fecha_actual),
									  "funcionamiento": funcionamiento.funcionamiento}
							encuestas_records.append(record)


			encuestas_dict["encuestas"]=encuestas_records
			return JsonResponse(encuestas_dict,  safe=False  )

		else:

			return JsonResponse({'resultado':'No hay encuestas pendientes.'},status=400)


class EncuestaViewList(generics.ListAPIView, generics.UpdateAPIView):
	"""Vista para que muestre una encuesta"""
	serializer_class = EncuestaSerializer
	http_method_names = ['get']

	def list(self, request, *args, **kwargs):
		id_e = self.kwargs['id_e']
		usuario = self.request.user
		responsable_comedor = usuario.groups.filter(name='Responsable Comedor').exists()
		if responsable_comedor:
			encuesta = Encuesta.objects.filter(id=id_e, responsable_comedor=responsable_comedor).values('id', 'fecha', 'comedor', 'organizacion', 'responsable_comedor', 'cantidad_rango_1', 'cantidad_rango_2', 'cantidad_rango_3', 'cantidad_rango_4', 'funcionamiento')
			#comidas = ComidaEncuesta.objects.filter(encuesta=id_e)
			#comidas = comidas.values('encuesta', 'comida').annotate(alimento=ArrayAgg('alimento', delimiter=', ', distinct=True)).values('comida', 'alimento')
			#return Response({'data': {
			#	'encuesta': encuesta,
			#	'comidas': comidas
			#}})
		#else:
		return Response({'data': {}})

class EncuestasViewList(generics.ListAPIView):

	serializer_class = ComidaEncuestaPostSerializer
	http_method_names = ['post']
	"""
	def list(self, request, *args, **kwargs):
		usuario = self.request.user
		responsable_comedor = usuario.groups.filter(name='Responsable Comedor').exists()
		if responsable_comedor:
			respuesta = {}
			encuestas = Encuesta.objects.filter(responsable_comedor=responsable_comedor).values('id', 'fecha', 'comedor', 'organizacion', 'responsable_comedor', 'cantidad_rango_1', 'cantidad_rango_2', 'cantidad_rango_3', 'cantidad_rango_4', 'funcionamiento')
			#for e in encuestas:
			#	comidas = ComidaEncuesta.objects.filter(encuesta=e['id'])
			#	comidas = comidas.values('encuesta', 'comida').annotate(alimento=ArrayAgg('alimento', delimiter=', ', distinct=True)).values('comida', 'alimento')
			#	respuesta.update({'encuesta': e, 'comidas': comidas})
			#return Response({'data': respuesta})
		#else:
		return Response({'data': {}})
	"""
	def post(self, request):
		encuesta = request.data['encuesta']
		comida1 = request.data['comida1']
		comida2 = request.data['comida2']
		comida3 = request.data['comida3']
		serializerComida1 = None
		serializerComida2 = None
		serializerComida3 = None
		usuario = self.request.user
		responsable_comedor = usuario.groups.filter(name='Responsable Comedor').exists()
		if responsable_comedor:
			if comida1['comida'] == 'null' and comida2['comida'] == 'null' and comida3['comida'] == 'null':
				return Response(
					{"res": "La encuesta debe tener al menos una comida"},
					status=status.HTTP_400_BAD_REQUEST
				)
			serializerEncuesta = EncuestaSerializer(data=encuesta)
			serializerEncuesta.is_valid(raise_exception=True)
			if comida1['comida']:
				if not comida1['alimento']:
					return Response(
						{"res": "Las comida1 tiene que tener al menos un alimento"},
						status=status.HTTP_400_BAD_REQUEST
					)
				data = {
					'alimento': comida1['alimento'],
					'comida': comida1['comida']
				}
				serializerComida1 = ComidaEncuestaSerializer(data=data)
				serializerComida1.is_valid(raise_exception=True)
			if comida2['comida']:
				if not comida2['alimento']:
					return Response(
						{"res": "Las comidas2 tiene que tener al menos un alimento"},
						status=status.HTTP_400_BAD_REQUEST
					)
				data = {
					'alimento': comida2['alimento'],
					'comida': comida2['comida'],
				}
				serializerComida2 = ComidaEncuestaSerializer(data=data)
				serializerComida2.is_valid(raise_exception=True)
			if comida3['comida']:
				if not comida3['alimento']:
					return Response(
						{"res": "Las comida3 tiene que tener al menos un alimento"},
						status=status.HTTP_400_BAD_REQUEST
					)
				data = {
					'alimento': comida3['alimento'],
					'comida': comida3['comida'],
				}
				serializerComida3 = ComidaEncuestaSerializer(data=data)
				serializerComida3.is_valid(raise_exception=True)
			serializerEncuesta.save()
			respuesta = {}
			respuesta['encuesta'] = serializerEncuesta.data
			if serializerComida1:
				for a in comida1['alimento']:
					data = {
						'alimento': a['alimento'],
						'encuesta': serializerEncuesta.data['id'],
						'comida': comida1['comida'],
						'cantidad': a['cantidad'],
						'unidad': a['unidad']
					}
					alimento = AlimentoEncuestaCompletoSerializer(data=data)
					alimento.is_valid(raise_exception=True)
					alimento.save()
				respuesta['comida1'] = serializerComida1.data
			if serializerComida2:
				for a in comida2['alimento']:
					data = {
						'alimento': a['alimento'],
						'encuesta': serializerEncuesta.data['id'],
						'comida': comida2['comida'],
						'cantidad': a['cantidad'],
						'unidad': a['unidad']
					}
					alimento = AlimentoEncuestaCompletoSerializer(data=data)
					alimento.is_valid(raise_exception=True)
					alimento.save()
				respuesta['comida2'] = serializerComida2.data
			if serializerComida3:
				for a in comida3['alimento']:
					data = {
						'alimento': a['alimento'],
						'encuesta': serializerEncuesta.data['id'],
						'comida': comida3['comida'],
						'cantidad': a['cantidad'],
						'unidad': a['unidad']
					}
					alimento = AlimentoEncuestaCompletoSerializer(data=data)
					alimento.is_valid(raise_exception=True)
					alimento.save()
				respuesta['comida3'] = serializerComida3.data
			return Response(data=respuesta, status=status.HTTP_201_CREATED)
		else:
			return Response(
				{"res": "El usuario no es un Responsable de Comedor"},
				status=status.HTTP_400_BAD_REQUEST
			)

class NoSeSirvioEncuestasView(generics.ListAPIView):

	serializer_class = NoSeSirvioEncuestaSerializer
	http_method_names = ['post']
	def post(self, request):
		if not Encuesta.objects.filter(comedor=request.data['comedor'], fecha=request.data['fecha'], funcionamiento=request.data['funcionamiento']):
			encuesta = self.get_serializer(data=request.data)
			encuesta.is_valid(raise_exception=True)
			encuesta.save()
			return Response(encuesta.data)
		else:
			return Response(
				{"res": "Esta encuesta ya tiene respuesta"},
				status=status.HTTP_400_BAD_REQUEST
			)
