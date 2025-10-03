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
		
		# Log para debuggear los datos recibidos
		print("=== DEBUG ENCUESTA POST ===")
		print("Request data keys:", list(request.data.keys()))
		print("Request data:", request.data)
		
		# Manejar tanto el formato antiguo (comida1, comida2, comida3) como el nuevo (comidas array)
		comidas_data = []
		
		if 'comidas' in request.data:
			# Nuevo formato: array de comidas
			comidas_data = request.data['comidas']
			print("Usando nuevo formato - comidas_data:", comidas_data)
		else:
			# Formato antiguo: comida1, comida2, comida3
			comida1 = request.data.get('comida1', {'comida': 'null', 'alimento': []})
			comida2 = request.data.get('comida2', {'comida': 'null', 'alimento': []})
			comida3 = request.data.get('comida3', {'comida': 'null', 'alimento': []})
			
			print("Usando formato antiguo:")
			print("comida1:", comida1)
			print("comida2:", comida2)
			print("comida3:", comida3)
			
			# Convertir formato antiguo a nuevo formato
			if comida1['comida'] != 'null':
				comidas_data.append(comida1)
			if comida2['comida'] != 'null':
				comidas_data.append(comida2)
			if comida3['comida'] != 'null':
				comidas_data.append(comida3)
		
		print("comidas_data final:", comidas_data)
		
		# Filtrar comidas vacías y duplicadas
		comidas_filtradas = []
		comidas_vistas = set()
		
		for comida in comidas_data:
			comida_id = comida.get('comida')
			alimentos = comida.get('alimento', [])
			
			# Solo agregar si tiene alimentos y no es duplicada
			if alimentos and len(alimentos) > 0 and comida_id not in comidas_vistas:
				comidas_filtradas.append(comida)
				comidas_vistas.add(comida_id)
				print(f"Comida {comida_id} agregada - alimentos: {len(alimentos)}")
			else:
				print(f"Comida {comida_id} filtrada - vacía o duplicada")
		
		print("comidas_filtradas:", comidas_filtradas)
		comidas_data = comidas_filtradas
		
		usuario = self.request.user
		responsable_comedor = usuario.groups.filter(name='Responsable Comedor').exists()
		if responsable_comedor:
			if len(comidas_data) == 0:
				return Response(
					{"res": "La encuesta debe tener al menos una comida"},
					status=status.HTTP_400_BAD_REQUEST
				)
			serializerEncuesta = EncuestaSerializer(data=encuesta)
			serializerEncuesta.is_valid(raise_exception=True)
			
			# Validar cada comida
			serializers_comidas = []
			for i, comida in enumerate(comidas_data):
				print(f"=== VALIDANDO COMIDA {i+1} ===")
				print(f"comida: {comida}")
				print(f"comida.get('alimento'): {comida.get('alimento')}")
				print(f"comida.get('alimento') is None: {comida.get('alimento') is None}")
				print(f"comida.get('alimento') == []: {comida.get('alimento') == []}")
				print(f"len(comida.get('alimento', [])): {len(comida.get('alimento', []))}")
				
				if not comida.get('alimento'):
					print(f"ERROR: La comida {i+1} no tiene alimentos")
					return Response(
						{"res": f"La comida {i+1} tiene que tener al menos un alimento"},
						status=status.HTTP_400_BAD_REQUEST
					)
				
				# Verificar si los alimentos tienen datos válidos
				alimentos = comida.get('alimento', [])
				print(f"alimentos: {alimentos}")
				print(f"len(alimentos): {len(alimentos)}")
				
				if len(alimentos) == 0:
					print(f"ERROR: La comida {i+1} tiene array de alimentos vacío")
					return Response(
						{"res": f"La comida {i+1} tiene que tener al menos un alimento"},
						status=status.HTTP_400_BAD_REQUEST
					)
				
				data = {
					'alimento': comida['alimento'],
					'comida': comida['comida']
				}
				print(f"data para serializer: {data}")
				
				serializer_comida = ComidaEncuestaSerializer(data=data)
				serializer_comida.is_valid(raise_exception=True)
				serializers_comidas.append(serializer_comida)
			serializerEncuesta.save()
			respuesta = {}
			respuesta['encuesta'] = serializerEncuesta.data
			
			# Guardar cada comida y sus alimentos
			for i, (comida, serializer_comida) in enumerate(zip(comidas_data, serializers_comidas)):
				print(f"=== GUARDANDO COMIDA {i+1} ===")
				print(f"comida: {comida}")
				print(f"comida['alimento']: {comida['alimento']}")
				
				for j, a in enumerate(comida['alimento']):
					print(f"--- ALIMENTO {j+1} ---")
					print(f"alimento: {a}")
					
					data = {
						'alimento': a['alimento'],
						'encuesta': serializerEncuesta.data['id'],
						'comida': comida['comida'],
						'cantidad': a['cantidad'],
						'unidad': a['unidad']
					}
					print(f"data para AlimentoEncuestaCompletoSerializer: {data}")
					
					alimento = AlimentoEncuestaCompletoSerializer(data=data)
					if not alimento.is_valid():
						print(f"ERROR en serializer de alimento: {alimento.errors}")
					alimento.is_valid(raise_exception=True)
					alimento.save()
					print(f"Alimento {j+1} guardado exitosamente")
				
				respuesta[f'comida{i+1}'] = serializer_comida.data
				print(f"Comida {i+1} guardada exitosamente")
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
