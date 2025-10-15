from django.shortcuts import render
from rest_framework import generics
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from .serializers import ComedorListaSerializer, ComedorListaLabelSerializer
from encuesta.models import Encuesta, AlimentoEncuesta
from django.db.models import Count, Sum, F, Q
from django.http import JsonResponse
from responsable_organizacion.models import ResponsableOrganizacion
from comedor.models import Comedor

# Create your views here.

# Consultar raciones del ultimo mes ------------------------------------------------------------------------------------

def racionesPorDia(comedor, fecha_inicio, fecha_fin):
	lista = Encuesta.objects.filter(comedor=comedor, fecha__range=(fecha_inicio, fecha_fin))
	lista = lista.values('fecha').annotate(cantidad=Sum(	F('cantidad_rango_1') + F('cantidad_rango_2') + F('cantidad_rango_3') + F('cantidad_rango_4'))).order_by('fecha')
	return lista

class RacionesMesViewList(generics.ListAPIView):

	serializer_class = ComedorListaSerializer
	http_method_names = ['get']

	def get(self, request, *args, **kwargs):
		comedor = kwargs['comedor']
		today = date.today()
		td = timedelta(29)
		lista = racionesPorDia(comedor, today-td, today)
		diccionario = {
			'comedor': comedor,
			'lista': list(lista)
		}
		return JsonResponse(diccionario, safe=False)

# Consultar raciones de la ultima semana -------------------------------------------------------------------------------
class RacionesSemanaViewList(generics.ListAPIView):

	serializer_class = ComedorListaSerializer
	http_method_names = ['get']

	def get(self, request, *args, **kwargs):
		comedor = kwargs['comedor']
		today = date.today()
		td = timedelta(6)
		lista = racionesPorDia(comedor, today - td, today)
		diccionario = {
			'comedor': comedor,
			'lista': list(lista)
		}
		return JsonResponse(diccionario, safe=False)

# Consultas de comidas del ultimo mes -----------------------------------------------------------------------------

def getComidaFecha(e):
	return e['comida__nombre'] + ' ' + str(e['encuesta__fecha'].year)+str(e['encuesta__fecha'].month)+str(e['encuesta__fecha'].day)
def getComidaDia(comedor, fecha_inicio, fecha_fin):
	# Obtenemos las comidas únicas por encuesta para evitar duplicar las cantidades
	comidas_unicas = AlimentoEncuesta.objects.filter(
		encuesta__fecha__range=(fecha_inicio, fecha_fin), 
		encuesta__comedor=comedor
	).values('encuesta', 'comida__nombre', 'encuesta__fecha', 'encuesta__funcionamiento').distinct()
	
	# Agrupamos las comidas por encuesta y funcionamiento para poder dividir las raciones
	from collections import defaultdict
	encuestas_comidas = defaultdict(lambda: defaultdict(list))
	
	for item in comidas_unicas:
		encuesta_id = item['encuesta']
		funcionamiento = item['encuesta__funcionamiento']
		comida_nombre = item['comida__nombre']
		fecha = item['encuesta__fecha']
		
		encuestas_comidas[encuesta_id][funcionamiento].append({
			'comida_nombre': comida_nombre,
			'fecha': fecha
		})
	
	# Luego creamos una lista de diccionarios con las cantidades correctas
	cantidad_raciones_comida_dias = []
	for encuesta_id, funcionamientos in encuestas_comidas.items():
		encuesta = Encuesta.objects.get(id=encuesta_id)
		total_comensales = encuesta.cantidad_rango_1 + encuesta.cantidad_rango_2 + encuesta.cantidad_rango_3 + encuesta.cantidad_rango_4
		
		for funcionamiento, comidas in funcionamientos.items():
			# Dividir las raciones entre la cantidad de comidas del mismo funcionamiento
			comidas_count = len(comidas)
			raciones_por_comida = total_comensales / comidas_count if comidas_count > 0 else total_comensales
			
			for comida_info in comidas:
				cantidad_raciones_comida_dias.append({
					'encuesta__fecha': comida_info['fecha'],
					'comida__nombre': comida_info['comida_nombre'],
					'cantidad': raciones_por_comida
				})
	
	# Agrupamos por fecha y comida, sumando las cantidades
	agrupado = defaultdict(float)
	for item in cantidad_raciones_comida_dias:
		key = (item['encuesta__fecha'], item['comida__nombre'])
		agrupado[key] += item['cantidad']
	
	# Obtenemos todas las fechas y comidas únicas
	fechas = sorted(set([item['encuesta__fecha'] for item in cantidad_raciones_comida_dias]))
	comidas = set([item['comida__nombre'] for item in cantidad_raciones_comida_dias])
	
	# Creamos la estructura de datos correcta: cada comida tiene un array de datos para cada fecha
	comida_semana = []
	for comida in comidas:
		datos_por_fecha = []
		for fecha in fechas:
			cantidad = agrupado.get((fecha, comida), 0)
			datos_por_fecha.append(round(cantidad, 2))  # Redondeamos a 2 decimales
		
		comida_semana.append({
			'label': comida,
			'data': datos_por_fecha,
		})
	
	return list(comida_semana), list(fechas)
class ComidasMesViewList(generics.ListAPIView):

	serializer_class = ComedorListaLabelSerializer
	http_method_names = ['get']

	def get(self, request, *args, **kwargs):
		comedor = kwargs['comedor']
		today = date.today()
		td = timedelta(29)
		lista = getComidaDia(comedor, today-td, today)
		diccionario = {
			'comedor': comedor,
			'labels': lista[1],
			'lista': lista[0]
		}
		return JsonResponse(diccionario, safe=False)

# Consultas de comidas de la ultima semana ----------------------------------------------------------------------------------

class ComidasSemanaViewList(generics.ListAPIView):

	serializer_class = ComedorListaLabelSerializer
	http_method_names = ['get']

	def get(self, request, *args, **kwargs):
		comedor = kwargs['comedor']
		today = date.today()
		td = timedelta(6)
		lista = getComidaDia(comedor, today-td, today)
		diccionario = {
			'comedor': comedor,
			'labels': lista[1],
			'lista': lista[0]
		}
		return JsonResponse(diccionario, safe=False)

# Reportes Nutricionales ------------------------------------------------------------------------------------

def calcular_nutrientes_por_encuesta(encuesta):
	"""Calcula los nutrientes promedio por comensal para una encuesta"""
	alimentos_encuesta = AlimentoEncuesta.objects.filter(encuesta=encuesta)
	total_comensales = encuesta.cantidad_rango_1 + encuesta.cantidad_rango_2 + encuesta.cantidad_rango_3 + encuesta.cantidad_rango_4
	
	if total_comensales == 0:
		return None
	
	nutrientes_por_comensal = {
		'hidratos': 0, 'proteinas': 0, 'grasasSaturadas': 0, 
		'grasasTotales': 0, 'kilocalorias': 0, 'sodio': 0
	}
	
	for alimento_encuesta in alimentos_encuesta:
		# Obtener la unidad y su equivalencia en gramos
		unidad = alimento_encuesta.unidad
		cantidad_unidades = float(alimento_encuesta.cantidad)
		
		# Convertir a gramos usando la equivalencia de la unidad
		if unidad.equivalencia_gramos:
			cantidad_gramos = cantidad_unidades * float(unidad.equivalencia_gramos)
		else:
			# Si no hay equivalencia en gramos, usar ml y asumir densidad 1g/ml
			cantidad_gramos = cantidad_unidades * float(unidad.equivalencia_ml)
		
		# Obtener nutrientes del alimento (por 100g)
		alimento = alimento_encuesta.alimento
		
		# Calcular nutrientes totales de este alimento
		nutrientes_alimento = {
			'hidratos': (float(alimento.hidratos_carbono) * cantidad_gramos) / 100,
			'proteinas': (float(alimento.proteinas) * cantidad_gramos) / 100,
			'grasasSaturadas': (float(alimento.grasas) * cantidad_gramos) / 100,
			'grasasTotales': (float(alimento.grasas_totales) * cantidad_gramos) / 100,
			'kilocalorias': (float(alimento.energia) * cantidad_gramos) / 100,
			'sodio': (float(alimento.sodio) * cantidad_gramos) / 100
		}
		
		# Sumar a los nutrientes totales
		for nutriente in nutrientes_por_comensal:
			nutrientes_por_comensal[nutriente] += nutrientes_alimento[nutriente]
	
	# Dividir por número de comensales para obtener nutrientes por comensal
	for nutriente in nutrientes_por_comensal:
		nutrientes_por_comensal[nutriente] = nutrientes_por_comensal[nutriente] / total_comensales
	
	return nutrientes_por_comensal

class ReportesNutricionalesMesViewList(generics.ListAPIView):
	"""Reportes nutricionales de los últimos 12 meses"""
	serializer_class = ComedorListaSerializer
	http_method_names = ['get']

	def get(self, request, *args, **kwargs):
		comedor_id = kwargs['comedor']
		
		# Obtener comedor
		try:
			comedor = Comedor.objects.get(id=comedor_id)
		except Comedor.DoesNotExist:
			return JsonResponse({'error': 'Comedor no encontrado'}, status=404)
		
		# Calcular fecha límite (12 meses atrás)
		today = date.today()
		td = relativedelta(months=-11)
		fecha_limite = today + td
		
		# Obtener encuestas de los últimos 12 meses
		encuestas_12_meses = Encuesta.objects.filter(
			comedor=comedor,
			fecha__range=(fecha_limite, today)
		).order_by('-fecha')
		
		# Calcular nutrientes por mes
		nutrientes_por_mes = {}
		for encuesta in encuestas_12_meses:
			mes_key = f"{encuesta.fecha.year}-{encuesta.fecha.month:02d}"
			if mes_key not in nutrientes_por_mes:
				nutrientes_por_mes[mes_key] = {
					'hidratos': 0, 'proteinas': 0, 'grasasSaturadas': 0, 
					'grasasTotales': 0, 'kilocalorias': 0, 'sodio': 0,
					'total_encuestas': 0
				}
			
			nutrientes = calcular_nutrientes_por_encuesta(encuesta)
			if nutrientes:
				for nutriente in nutrientes_por_mes[mes_key]:
					if nutriente in nutrientes:
						nutrientes_por_mes[mes_key][nutriente] += nutrientes[nutriente]
				nutrientes_por_mes[mes_key]['total_encuestas'] += 1
		
		# Calcular promedios por mes
		promedios_mes = []
		for mes, datos in nutrientes_por_mes.items():
			if datos['total_encuestas'] > 0:
				promedio = {
					'mes': mes,
					'hidratos': round(datos['hidratos'] / datos['total_encuestas'], 2),
					'proteinas': round(datos['proteinas'] / datos['total_encuestas'], 2),
					'grasasSaturadas': round(datos['grasasSaturadas'] / datos['total_encuestas'], 2),
					'grasasTotales': round(datos['grasasTotales'] / datos['total_encuestas'], 2),
					'kilocalorias': round(datos['kilocalorias'] / datos['total_encuestas'], 2),
					'sodio': round(datos['sodio'] / datos['total_encuestas'], 2)
				}
				promedios_mes.append(promedio)
		
		# Ordenar por fecha (mes-año)
		promedios_mes.sort(key=lambda x: x['mes'])
		
		diccionario = {
			'comedor': comedor_id,
			'lista': promedios_mes
		}
		return JsonResponse(diccionario, safe=False)

class ReportesNutricionalesSemanaViewList(generics.ListAPIView):
	"""Reportes nutricionales de los últimos 7 días"""
	serializer_class = ComedorListaSerializer
	http_method_names = ['get']

	def get(self, request, *args, **kwargs):
		comedor_id = kwargs['comedor']
		
		# Obtener comedor
		try:
			comedor = Comedor.objects.get(id=comedor_id)
		except Comedor.DoesNotExist:
			return JsonResponse({'error': 'Comedor no encontrado'}, status=404)
		
		# Calcular fecha límite (7 días atrás)
		today = date.today()
		td = timedelta(days=-6)
		fecha_limite = today + td
		
		# Obtener encuestas de los últimos 7 días
		encuestas_7_dias = Encuesta.objects.filter(
			comedor=comedor,
			fecha__range=(fecha_limite, today)
		).order_by('-fecha')
		
		# Calcular nutrientes por día
		nutrientes_por_dia = {}
		for encuesta in encuestas_7_dias:
			dia_key = str(encuesta.fecha)
			if dia_key not in nutrientes_por_dia:
				nutrientes_por_dia[dia_key] = {
					'hidratos': 0, 'proteinas': 0, 'grasasSaturadas': 0, 
					'grasasTotales': 0, 'kilocalorias': 0, 'sodio': 0,
					'total_encuestas': 0
				}
			
			nutrientes = calcular_nutrientes_por_encuesta(encuesta)
			if nutrientes:
				for nutriente in nutrientes_por_dia[dia_key]:
					if nutriente in nutrientes:
						nutrientes_por_dia[dia_key][nutriente] += nutrientes[nutriente]
				nutrientes_por_dia[dia_key]['total_encuestas'] += 1
		
		# Calcular promedios por día
		promedios_dia = []
		for dia, datos in nutrientes_por_dia.items():
			if datos['total_encuestas'] > 0:
				promedio = {
					'dia': dia,
					'hidratos': round(datos['hidratos'] / datos['total_encuestas'], 2),
					'proteinas': round(datos['proteinas'] / datos['total_encuestas'], 2),
					'grasasSaturadas': round(datos['grasasSaturadas'] / datos['total_encuestas'], 2),
					'grasasTotales': round(datos['grasasTotales'] / datos['total_encuestas'], 2),
					'kilocalorias': round(datos['kilocalorias'] / datos['total_encuestas'], 2),
					'sodio': round(datos['sodio'] / datos['total_encuestas'], 2)
				}
				promedios_dia.append(promedio)
		
		# Ordenar por fecha (día)
		promedios_dia.sort(key=lambda x: x['dia'])
		
		diccionario = {
			'comedor': comedor_id,
			'lista': promedios_dia
		}
		return JsonResponse(diccionario, safe=False)
