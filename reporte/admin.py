from collections import Counter, defaultdict
from datetime import date, timedelta
from itertools import chain

from dateutil.relativedelta import relativedelta
from django.db.models import Count, Sum, F, Q
from .models import ReporteNutricional, ReportesGenerales, ReportesRaciones, ReportesNutricionales
from django.contrib import admin
from comedor.models import Comedor
from encuesta.models import Encuesta, AlimentoEncuesta
from comida.models import Comida
from responsable_organizacion.models import ResponsableOrganizacion


class ReportesGeneralesAdmin(admin.ModelAdmin):

	change_list_template = 'reportes_generales.html'

	def changelist_view(self, request, extra_context=None):

		response = super().changelist_view(
			request,
			extra_context=extra_context,
		)

		r = ResponsableOrganizacion.objects.filter(responsable=request.user).values('organizacion')
		if (request.user.is_superuser or request.user.groups.filter(name='Administrador').exists()):
			lc = Comedor.objects.all()
		else:
			lc = Comedor.objects.filter(
				Q(responsable_comedor=request.user) |
				Q(organizacion_regional__in=r) |
				Q(organizacion_regional__organizacion_superior__in=r)
			)

		# Comedores por provincia
		comedores_qs = lc.values('provincia__nombre').annotate(dcount=Count('provincia__nombre')).order_by()
		comedores = list(comedores_qs)
		response.context_data['comedores_provincia'] = comedores

		# Listado de provincias
		response.context_data['provincias'] = comedores_qs.values('provincia__nombre')

		# Listado de departamentos

		comedores = lc.values('provincia__nombre', 'departamento__nombre').annotate(dcount=Count('departamento__nombre')).order_by()
		comedores = list(comedores)
		response.context_data['comedores_departamento'] = comedores

		# Listado de gobiernos_locales

		comedores = lc.values('provincia__nombre', 'departamento__nombre', 'gobierno_local__nombre').annotate(dcount=Count('gobierno_local__nombre')).order_by()
		comedores = list(comedores)
		response.context_data['comedores_gobierno_local'] = comedores

		# Listado de gobiernos_locales

		comedores = lc.values('provincia__nombre', 'departamento__nombre', 'gobierno_local__nombre', 'localidad__nombre').annotate(dcount=Count('localidad__nombre')).order_by()
		comedores = list(comedores)
		response.context_data['comedores_localidad'] = comedores

		# Comedores por organizacion

		comedores_qs_or = lc.filter(organizacion_regional__es_organizacion_regional=True).values('organizacion_regional__organizacion_superior__nombre').values_list('organizacion_regional__organizacion_superior__nombre', flat=True)
		comedores_qs_o = lc.filter(organizacion_regional__es_organizacion_regional=False).values('organizacion_regional__nombre').values_list('organizacion_regional__nombre', flat=True)
		comedores = list(comedores_qs_or) + list(comedores_qs_o)
		comedores = dict(Counter(comedores))

		c = []
		for a in comedores:
			c.append({
				'organizacion': a,
				'dcount': comedores[a],
			})

		response.context_data['comedores_organizacion'] = c

		# Listado de organizaciones

		comedores = lc.filter(organizacion_regional__es_organizacion_regional=True).values('organizacion_regional__organizacion_superior__nombre').values_list('organizacion_regional__organizacion_superior__nombre', flat=True)
		comedores = list(set(comedores))
		response.context_data['comedores_organizaciones'] = comedores

		# Listado de organizaciones regionales

		comedores = lc.filter(organizacion_regional__es_organizacion_regional=True).values('organizacion_regional__organizacion_superior__nombre', 'organizacion_regional__nombre').annotate(dcount=Count('organizacion_regional__nombre')).order_by()
		comedores = list(comedores)
		response.context_data['comedores_organizacion_regional'] = comedores

		return response


class ReportesRacionesAdmin(admin.ModelAdmin):

	change_list_template = 'reportes_raciones.html'

	def getMesAñoComida(self, e):
		mes = e['mes']
		if mes < 10:
			mes = '0' + str(mes)
		else:
			mes = str(mes)
		return str(e['año']) + ' ' + mes + ' ' + e['comida']

	def getAñoMes(self, e):
		e = e.split('/')
		mes = e[0]
		if int(mes) < 10:
			mes = '0' + str(mes)
		else:
			mes = str(mes)
		return e[1] + ' ' + mes

	def getComidaMesAño(self, e):
		mes = e['encuesta__fecha__month']
		if mes < 10:
			mes = '0' + str(mes)
		else:
			mes = str(mes)
		return e['comida__nombre'] + ' ' + str(e['encuesta__fecha__year']) + ' ' + mes

	def getFechaComida(self, e):
		return str(e['fecha'].year)+str(e['fecha'].month)+str(e['fecha'].day) + ' ' + e['comida']

	def getComidaFecha(self, e):
		return e['comida__nombre'] + ' ' + str(e['encuesta__fecha'].year)+str(e['encuesta__fecha'].month)+str(e['encuesta__fecha'].day)

	def changelist_view(self, request, extra_context=None):

		response = super().changelist_view(
			request,
			extra_context=extra_context,
		)

		r = ResponsableOrganizacion.objects.filter(responsable=request.user).values('organizacion')
		if (request.user.is_superuser or request.user.groups.filter(name='Administrador').exists()):
			lc = Comedor.objects.all()
		else:
			lc = Comedor.objects.filter(
				Q(responsable_comedor=request.user) |
				Q(organizacion_regional__in=r) |
				Q(organizacion_regional__organizacion_superior__in=r)
			)

		# Encuestas de los ultimos 12 meses ----------------------------------------------------------------------------

		today = date.today()
		td = relativedelta(months=-11)
		fecha = today + td
		fecha_limite = date(day=1, month=fecha.month, year=fecha.year)

		r_mes_total = Encuesta.objects.filter(comedor__in=lc, fecha__range=(fecha_limite, today))

		# Cantidad de raciones por mes de los ultimos 12 meses
		cantidad_raciones_meses = r_mes_total.values('fecha__year', 'fecha__month', 'cantidad_rango_1', 'cantidad_rango_2', 'cantidad_rango_3', 'cantidad_rango_4')
		cantidad_raciones_meses = cantidad_raciones_meses.values('fecha__year', 'fecha__month').annotate(cantidad=Sum(F('cantidad_rango_1') + F('cantidad_rango_2') + F('cantidad_rango_3') + F('cantidad_rango_4'))).order_by('fecha__year', 'fecha__month')
		response.context_data['raciones_mes'] = cantidad_raciones_meses

		# Cantidad de raciones por funcionamiento de los ultimos 12 meses
		cantidad_raciones_funcionamiento_meses = r_mes_total.values('fecha__year', 'fecha__month', 'cantidad_rango_1', 'cantidad_rango_2', 'cantidad_rango_3', 'cantidad_rango_4', 'funcionamiento')
		cantidad_raciones_funcionamiento_meses = cantidad_raciones_funcionamiento_meses.values('fecha__year', 'fecha__month', 'funcionamiento').annotate(cantidad=Sum(F('cantidad_rango_1') + F('cantidad_rango_2') + F('cantidad_rango_3') + F('cantidad_rango_4')))
		response.context_data['raciones_mes_funcionamiento'] = cantidad_raciones_funcionamiento_meses

		# Cantidad de raciones por rango etario de los ultimos 12 meses
		cantidad_raciones_rango_etario_meses = r_mes_total.values('fecha__year', 'fecha__month', 'cantidad_rango_1', 'cantidad_rango_2', 'cantidad_rango_3', 'cantidad_rango_4')
		cantidad_raciones_rango_etario_meses = cantidad_raciones_rango_etario_meses.values('fecha__year', 'fecha__month').annotate(cantidad_rango_1=Sum(F('cantidad_rango_1')), cantidad_rango_2=Sum(F('cantidad_rango_2')), cantidad_rango_3=Sum(F('cantidad_rango_3')), cantidad_rango_4=Sum(F('cantidad_rango_4')))
		response.context_data['raciones_mes_rango_etario'] = cantidad_raciones_rango_etario_meses

		# Cantidad de raciones por comida de los ultimos 12 meses
		# Usamos una aproximación diferente: obtenemos las comidas únicas por encuesta
		# y luego sumamos las cantidades de comensales divididas por funcionamiento
		
		# Primero obtenemos todas las comidas únicas por encuesta con etapa_comida
		comidas_unicas = AlimentoEncuesta.objects.filter(
			encuesta__fecha__range=(fecha_limite, today), 
			encuesta__comedor__in=lc
		).values('encuesta', 'comida__nombre', 'encuesta__fecha__year', 'encuesta__fecha__month', 'etapa_comida').distinct()
		
		# Agrupamos las comidas por encuesta y etapa_comida para poder dividir las raciones
		encuestas_comidas_meses = defaultdict(lambda: defaultdict(list))
		
		for item in comidas_unicas:
			encuesta_id = item['encuesta']
			etapa_comida = item['etapa_comida']
			comida_nombre = item['comida__nombre']
			year = item['encuesta__fecha__year']
			month = item['encuesta__fecha__month']
			
			encuestas_comidas_meses[encuesta_id][etapa_comida].append({
				'comida_nombre': comida_nombre,
				'year': year,
				'month': month
			})
		
		# Luego creamos una lista de diccionarios con las cantidades correctas
		cantidad_raciones_comida_meses = []
		for encuesta_id, etapas_comida in encuestas_comidas_meses.items():
			encuesta = Encuesta.objects.get(id=encuesta_id)
			total_comensales = encuesta.cantidad_rango_1 + encuesta.cantidad_rango_2 + encuesta.cantidad_rango_3 + encuesta.cantidad_rango_4
			
			for etapa_comida, comidas in etapas_comida.items():
				# Dividir los comensales entre las comidas de la misma etapa
				# Si hay 2 comensales y 2 entradas: cada entrada = 1 comensal
				comidas_count = len(comidas)
				if comidas_count > 0:
					# Calcular cuántos comensales come cada comida
					comensales_base = total_comensales // comidas_count  # División entera
					comensales_extra = total_comensales % comidas_count   # Resto para distribuir
					
					for i, comida_info in enumerate(comidas):
						# Las primeras 'comensales_extra' comidas reciben un comensal adicional
						raciones_por_comida = comensales_base + (1 if i < comensales_extra else 0)
						
						cantidad_raciones_comida_meses.append({
							'encuesta__fecha__year': comida_info['year'],
							'encuesta__fecha__month': comida_info['month'],
							'comida__nombre': comida_info['comida_nombre'],
							'cantidad': raciones_por_comida
						})
				else:
					# Si no hay comidas, no agregamos nada
					pass
		
		# Agrupamos por fecha y comida, sumando las cantidades
		agrupado = defaultdict(float)
		for item in cantidad_raciones_comida_meses:
			key = (item['encuesta__fecha__year'], item['encuesta__fecha__month'], item['comida__nombre'])
			agrupado[key] += item['cantidad']
		
		# Convertimos a la estructura esperada
		cantidad_raciones_comida_meses = [
			{
				'encuesta__fecha__year': year,
				'encuesta__fecha__month': month,
				'comida__nombre': comida,
				'cantidad': round(cantidad, 2)
			}
			for (year, month, comida), cantidad in agrupado.items()
		]
		cantidad_raciones_comida_meses.sort(key=lambda x: (x['encuesta__fecha__year'], x['encuesta__fecha__month'], x['comida__nombre']))
		comidas = set([item['comida__nombre'] for item in cantidad_raciones_comida_meses])
		fechas_bd = set([(item['encuesta__fecha__month'], item['encuesta__fecha__year']) for item in cantidad_raciones_comida_meses])
		# No necesitamos agregar ceros para 12 meses ya que tenemos los datos correctos
		fechas = [str(f[0])+'/'+str(f[1]) for f in fechas_bd]
		fechas.sort(key=self.getAñoMes)
		response.context_data['raciones_comida_mes'] = cantidad_raciones_comida_meses
		response.context_data['fechas_mes'] = fechas

		# Encuestas de los ultimos 30 dias -----------------------------------------------------------------------------

		today = date.today()
		td = timedelta(29)
		raciones_30_dias_total = Encuesta.objects.filter(comedor__in=lc, fecha__range=(today - td, today))
		raciones_30_dias_total = raciones_30_dias_total.values('fecha').annotate(cantidad=Sum(F('cantidad_rango_1') + F('cantidad_rango_2') + F('cantidad_rango_3') + F('cantidad_rango_4'))).order_by('fecha')
		response.context_data['raciones_dia'] = raciones_30_dias_total

		# Cantidad de raciones de los ultimos 7 dias -------------------------------------------------------------------

		today = date.today()
		td = timedelta(6)
		fecha = today - td
		r_semana_total = Encuesta.objects.filter(comedor__in=lc, fecha__range=(fecha, today))

		# Cantidad de raciones por funcionamiento de los ultimos 7 dias

		cantidad_raciones_funcionamiento_dias = r_semana_total.values('fecha', 'cantidad_rango_1', 'cantidad_rango_2', 'cantidad_rango_3', 'cantidad_rango_4', 'funcionamiento')
		cantidad_raciones_funcionamiento_dias = cantidad_raciones_funcionamiento_dias.values('fecha', 'funcionamiento').annotate(cantidad=Sum(F('cantidad_rango_1') + F('cantidad_rango_2') + F('cantidad_rango_3') + F('cantidad_rango_4')))
		response.context_data['raciones_semana_funcionamiento'] = cantidad_raciones_funcionamiento_dias

		# Cantidad de raciones por rango etario de los ultimos 7 dias
		cantidad_raciones_rango_etario_dias = r_semana_total.values('fecha', 'cantidad_rango_1', 'cantidad_rango_2', 'cantidad_rango_3', 'cantidad_rango_4')
		cantidad_raciones_rango_etario_dias = cantidad_raciones_rango_etario_dias.values('fecha').annotate(cantidad_rango_1=Sum(F('cantidad_rango_1')), cantidad_rango_2=Sum(F('cantidad_rango_2')), cantidad_rango_3=Sum(F('cantidad_rango_3')), cantidad_rango_4=Sum(F('cantidad_rango_4')))
		response.context_data['raciones_semana_rango_etario'] = cantidad_raciones_rango_etario_dias

		# Cantidad de raciones por comida de los ultimos 7 dias
		# Obtenemos las comidas únicas por encuesta con funcionamiento
		comidas_unicas_dias = AlimentoEncuesta.objects.filter(
			encuesta__fecha__range=(fecha, today), 
			encuesta__comedor__in=lc
		).values('encuesta', 'comida__nombre', 'encuesta__fecha', 'encuesta__funcionamiento').distinct()
		
		# Agrupamos las comidas por encuesta y funcionamiento para poder dividir las raciones
		encuestas_comidas_dias = defaultdict(lambda: defaultdict(list))
		
		for item in comidas_unicas_dias:
			encuesta_id = item['encuesta']
			funcionamiento = item['encuesta__funcionamiento']
			comida_nombre = item['comida__nombre']
			fecha_item = item['encuesta__fecha']
			
			encuestas_comidas_dias[encuesta_id][funcionamiento].append({
				'comida_nombre': comida_nombre,
				'fecha': fecha_item
			})
		
		# Luego creamos una lista de diccionarios con las cantidades correctas
		cantidad_raciones_comida_dias = []
		for encuesta_id, funcionamientos in encuestas_comidas_dias.items():
			encuesta = Encuesta.objects.get(id=encuesta_id)
			total_comensales = encuesta.cantidad_rango_1 + encuesta.cantidad_rango_2 + encuesta.cantidad_rango_3 + encuesta.cantidad_rango_4
			
			for funcionamiento, comidas in funcionamientos.items():
				# Cada comida debe contar las raciones completas de todos los comensales
				# No dividimos entre la cantidad de comidas porque cada comida es consumida por todos los comensales
				raciones_por_comida = total_comensales  # Cada comida tiene las raciones de todos los comensales
				
				for comida_info in comidas:
					cantidad_raciones_comida_dias.append({
						'encuesta__fecha': comida_info['fecha'],
						'comida__nombre': comida_info['comida_nombre'],
						'cantidad': raciones_por_comida
					})
		
		# Agrupamos por fecha y comida, sumando las cantidades
		agrupado_dias = defaultdict(float)
		for item in cantidad_raciones_comida_dias:
			key = (item['encuesta__fecha'], item['comida__nombre'])
			agrupado_dias[key] += item['cantidad']
		
		# Convertimos a la estructura esperada
		cantidad_raciones_comida_dias = [
			{
				'encuesta__fecha': fecha_item,
				'comida__nombre': comida,
				'cantidad': round(cantidad, 2)
			}
			for (fecha_item, comida), cantidad in agrupado_dias.items()
		]
		cantidad_raciones_comida_dias.sort(key=lambda x: (x['encuesta__fecha'], x['comida__nombre']))
		comidas = set([item['comida__nombre'] for item in cantidad_raciones_comida_dias])
		fechas = set([item['encuesta__fecha'] for item in cantidad_raciones_comida_dias])
		# No necesitamos agregar ceros para 7 días ya que tenemos los datos correctos
		response.context_data['raciones_comida_semana'] = cantidad_raciones_comida_dias
		response.context_data['fechas_semana'] = fechas

		return response

admin.site.register(ReportesGenerales, ReportesGeneralesAdmin)
admin.site.register(ReportesRaciones, ReportesRacionesAdmin)


# Comentamos el admin del modelo individual para ocultarlo completamente
# class ReporteNutricionalAdmin(admin.ModelAdmin):
# 	list_display = ['fecha', 'comedor', 'organizacion', 'encuesta']
# 	search_fields = ('comedor',)
# 	list_filter=('fecha','organizacion','comedor')

class ReportesNutricionalesAdmin(admin.ModelAdmin):
	change_list_template = 'reportes_nutricionales.html'

	def changelist_view(self, request, extra_context=None):
		response = super().changelist_view(
			request,
			extra_context=extra_context,
		)

		r = ResponsableOrganizacion.objects.filter(responsable=request.user).values('organizacion')
		if (request.user.is_superuser or request.user.groups.filter(name='Administrador').exists()):
			lc = Comedor.objects.all()
		else:
			lc = Comedor.objects.filter(
				Q(responsable_comedor=request.user) |
				Q(organizacion_regional__in=r) |
				Q(organizacion_regional__organizacion_superior__in=r)
			)

		# CÁLCULO AUTOMÁTICO DE NUTRIENTES BASADO EN ENCUESTAS
		today = date.today()
		td = relativedelta(months=-11)
		fecha_limite = today + td

		print(f"\n=== INICIO CÁLCULO NUTRICIONAL ===")
		print(f"Fecha límite: {fecha_limite}")
		print(f"Fecha actual: {today}")

		# Obtener todas las encuestas de los últimos 12 meses
		encuestas_12_meses = Encuesta.objects.filter(
			comedor__in=lc,
			fecha__range=(fecha_limite, today)
		).order_by('-fecha')
		
		print(f"Total encuestas encontradas: {encuestas_12_meses.count()}")

		# Calcular nutrientes por mes
		nutrientes_por_mes = {}
		for encuesta in encuestas_12_meses:
			mes_key = f"{encuesta.fecha.year}-{encuesta.fecha.month:02d}"
			if mes_key not in nutrientes_por_mes:
				nutrientes_por_mes[mes_key] = {
					'hidratos': 0, 'proteinas': 0, 'grasasSaturadas': 0, 
					'grasasTotales': 0, 'kilocalorias': 0, 'sodio': 0, 'porciones': 0,
					'total_comensales': 0, 'total_encuestas': 0
				}
			
			print(f"\n--- ENCUESTA {encuesta.id} - {encuesta.fecha} ---")
			
			# Obtener alimentos de esta encuesta
			alimentos_encuesta = AlimentoEncuesta.objects.filter(encuesta=encuesta)
			print(f"Alimentos en encuesta: {alimentos_encuesta.count()}")
			
			# Calcular total de comensales
			total_comensales = encuesta.cantidad_rango_1 + encuesta.cantidad_rango_2 + encuesta.cantidad_rango_3 + encuesta.cantidad_rango_4
			print(f"Comensales: {total_comensales} (rango1:{encuesta.cantidad_rango_1}, rango2:{encuesta.cantidad_rango_2}, rango3:{encuesta.cantidad_rango_3}, rango4:{encuesta.cantidad_rango_4})")
			
			if total_comensales > 0:
				# Calcular nutrientes por comensal
				nutrientes_por_comensal = {'hidratos': 0, 'proteinas': 0, 'grasasSaturadas': 0, 
											'grasasTotales': 0, 'kilocalorias': 0, 'sodio': 0}
				
				for alimento_encuesta in alimentos_encuesta:
					# Obtener la unidad y su equivalencia en gramos
					unidad = alimento_encuesta.unidad
					cantidad_unidades = float(alimento_encuesta.cantidad)
					
					print(f"  Alimento: {alimento_encuesta.alimento.nombre}")
					print(f"  Cantidad: {cantidad_unidades} {unidad.nombre}")
					print(f"  Equivalencia gramos: {unidad.equivalencia_gramos}")
					print(f"  Equivalencia ml: {unidad.equivalencia_ml}")
					
					# Convertir a gramos usando la equivalencia de la unidad
					if unidad.equivalencia_gramos:
						cantidad_gramos = cantidad_unidades * float(unidad.equivalencia_gramos)
						print(f"  Conversión: {cantidad_unidades} × {unidad.equivalencia_gramos} = {cantidad_gramos}g")
					else:
						# Si no hay equivalencia en gramos, usar ml y asumir densidad 1g/ml
						cantidad_gramos = cantidad_unidades * float(unidad.equivalencia_ml)
						print(f"  Conversión: {cantidad_unidades} × {unidad.equivalencia_ml} = {cantidad_gramos}g (ml)")
					
					# Obtener nutrientes del alimento (por 100g)
					alimento = alimento_encuesta.alimento
					print(f"  Nutrientes por 100g: H:{alimento.hidratos_carbono}, P:{alimento.proteinas}, G:{alimento.grasas}, GT:{alimento.grasas_totales}, E:{alimento.energia}, S:{alimento.sodio}")
					
					# Calcular nutrientes totales de este alimento
					nutrientes_alimento = {
						'hidratos': (float(alimento.hidratos_carbono) * cantidad_gramos) / 100,
						'proteinas': (float(alimento.proteinas) * cantidad_gramos) / 100,
						'grasasSaturadas': (float(alimento.grasas) * cantidad_gramos) / 100,
						'grasasTotales': (float(alimento.grasas_totales) * cantidad_gramos) / 100,
						'kilocalorias': (float(alimento.energia) * cantidad_gramos) / 100,
						'sodio': (float(alimento.sodio) * cantidad_gramos) / 100
					}
					
					print(f"  Nutrientes totales: H:{nutrientes_alimento['hidratos']:.2f}, P:{nutrientes_alimento['proteinas']:.2f}, G:{nutrientes_alimento['grasasSaturadas']:.2f}, GT:{nutrientes_alimento['grasasTotales']:.2f}, E:{nutrientes_alimento['kilocalorias']:.2f}, S:{nutrientes_alimento['sodio']:.2f}")
					
					# Sumar a los nutrientes totales
					for nutriente in nutrientes_por_comensal:
						nutrientes_por_comensal[nutriente] += nutrientes_alimento[nutriente]
				
				print(f"  Nutrientes totales comida: H:{nutrientes_por_comensal['hidratos']:.2f}, P:{nutrientes_por_comensal['proteinas']:.2f}, G:{nutrientes_por_comensal['grasasSaturadas']:.2f}, GT:{nutrientes_por_comensal['grasasTotales']:.2f}, E:{nutrientes_por_comensal['kilocalorias']:.2f}, S:{nutrientes_por_comensal['sodio']:.2f}")
				
				# Dividir por número de comensales para obtener nutrientes por comensal
				for nutriente in nutrientes_por_comensal:
					nutrientes_por_comensal[nutriente] = nutrientes_por_comensal[nutriente] / total_comensales
				
				print(f"  Nutrientes por comensal: H:{nutrientes_por_comensal['hidratos']:.2f}, P:{nutrientes_por_comensal['proteinas']:.2f}, G:{nutrientes_por_comensal['grasasSaturadas']:.2f}, GT:{nutrientes_por_comensal['grasasTotales']:.2f}, E:{nutrientes_por_comensal['kilocalorias']:.2f}, S:{nutrientes_por_comensal['sodio']:.2f}")
				
				# Sumar al mes
				for nutriente in nutrientes_por_mes[mes_key]:
					if nutriente in nutrientes_por_comensal:
						nutrientes_por_mes[mes_key][nutriente] += nutrientes_por_comensal[nutriente]
				
				nutrientes_por_mes[mes_key]['total_comensales'] += total_comensales
				nutrientes_por_mes[mes_key]['total_encuestas'] += 1

		# Calcular promedios por mes
		promedios_mes = []
		print(f"\n=== RESUMEN POR MES ===")
		for mes, datos in nutrientes_por_mes.items():
			if datos['total_encuestas'] > 0:
				promedio = {
					'mes': mes,
					'hidratos': round(datos['hidratos'] / datos['total_encuestas'], 2),
					'proteinas': round(datos['proteinas'] / datos['total_encuestas'], 2),
					'grasasSaturadas': round(datos['grasasSaturadas'] / datos['total_encuestas'], 2),
					'grasasTotales': round(datos['grasasTotales'] / datos['total_encuestas'], 2),
					'kilocalorias': round(datos['kilocalorias'] / datos['total_encuestas'], 2),
					'sodio': round(datos['sodio'] / datos['total_encuestas'], 2),
					'porciones': round(datos['total_comensales'] / datos['total_encuestas'], 2)
				}
				print(f"Mes {mes}: {datos['total_encuestas']} encuestas, {datos['total_comensales']} comensales")
				print(f"  Promedio por comensal: H:{promedio['hidratos']:.2f}, P:{promedio['proteinas']:.2f}, G:{promedio['grasasSaturadas']:.2f}, GT:{promedio['grasasTotales']:.2f}, E:{promedio['kilocalorias']:.2f}, S:{promedio['sodio']:.2f}")
				promedios_mes.append(promedio)
		
		# Ordenar por fecha (mes-año)
		promedios_mes.sort(key=lambda x: x['mes'])
		print(f"\n=== FIN CÁLCULO NUTRICIONAL ===")

		# CÁLCULO PARA ÚLTIMOS 7 DÍAS
		td_7 = timedelta(days=-6)
		fecha_7 = today + td_7
		encuestas_7_dias = Encuesta.objects.filter(
			comedor__in=lc,
			fecha__range=(fecha_7, today)
		).order_by('-fecha')

		# Calcular nutrientes por día
		nutrientes_por_dia = {}
		for encuesta in encuestas_7_dias:
			dia_key = str(encuesta.fecha)
			if dia_key not in nutrientes_por_dia:
				nutrientes_por_dia[dia_key] = {
					'hidratos': 0, 'proteinas': 0, 'grasasSaturadas': 0, 
					'grasasTotales': 0, 'kilocalorias': 0, 'sodio': 0, 'porciones': 0,
					'total_comensales': 0, 'total_encuestas': 0
				}
			
			# Obtener alimentos de esta encuesta
			alimentos_encuesta = AlimentoEncuesta.objects.filter(encuesta=encuesta)
			
			# Calcular total de comensales
			total_comensales = encuesta.cantidad_rango_1 + encuesta.cantidad_rango_2 + encuesta.cantidad_rango_3 + encuesta.cantidad_rango_4
			
			if total_comensales > 0:
				# Calcular nutrientes por comensal
				nutrientes_por_comensal = {'hidratos': 0, 'proteinas': 0, 'grasasSaturadas': 0, 
											'grasasTotales': 0, 'kilocalorias': 0, 'sodio': 0}
				
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
				
				# Sumar al día
				for nutriente in nutrientes_por_dia[dia_key]:
					if nutriente in nutrientes_por_comensal:
						nutrientes_por_dia[dia_key][nutriente] += nutrientes_por_comensal[nutriente]
				
				nutrientes_por_dia[dia_key]['total_comensales'] += total_comensales
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
					'sodio': round(datos['sodio'] / datos['total_encuestas'], 2),
					'porciones': round(datos['total_comensales'] / datos['total_encuestas'], 2)
				}
				promedios_dia.append(promedio)
		
		# Ordenar por fecha (día)
		promedios_dia.sort(key=lambda x: x['dia'])

		response.context_data['promedios_mes'] = promedios_mes
		response.context_data['promedios_dia'] = promedios_dia
		response.context_data['total_reportes'] = encuestas_12_meses.count()

		return response

# admin.site.register(ReporteNutricional, ReporteNutricionalAdmin)  # Oculto el modelo individual
admin.site.register(ReportesNutricionales, ReportesNutricionalesAdmin)
