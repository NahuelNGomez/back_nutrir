from django.contrib import admin

from alimento.models import Alimento
from reporte.models import ReporteNutricional
from .models import Encuesta, AlimentoEncuesta, NoSeSirvioEncuesta
from responsable_organizacion.models import ResponsableOrganizacion
from comedor.models import Comedor


# Por ahora, luego se bloquea la creacion del back

class AlimentoEncuestaInline(admin.TabularInline):
	model = AlimentoEncuesta
	fields = ['comida', 'alimento', 'cantidad', 'unidad']
	# readonly_fields = ['comida', 'alimento', 'cantidad']

	def __init__(self, *args, **kwargs):
		super(AlimentoEncuestaInline, self).__init__(*args, **kwargs)
		self.can_delete = False

class EncuestaAdmin(admin.ModelAdmin):

	list_display = ['fecha', 'comedor', 'organizacion', ]
	search_fields = ('fecha', 'comedor', 'organizacion', )
	list_filter = ('comedor', 'organizacion', 'funcionamiento')
	inlines = [AlimentoEncuestaInline]

	def get_queryset(self, request):
		qs = super(EncuestaAdmin, self).get_queryset(request)
		if not request.user.is_superuser:
			organizaciones = ResponsableOrganizacion.objects.filter(responsable=request.user).values('organizacion')
			comedores = Comedor.objects.filter(organizacion_regional__in=organizaciones)
			qs = qs.filter(id__in=comedores).distinct()
		return qs
	
	def save_model(self, request, obj, form, change):
		super().save_model(request, obj, form, change)
		# Agregado para registrar el impacto nutricional de la comida
		raciones = obj.cantidad_rango_1 + obj.cantidad_rango_2 + obj.cantidad_rango_3 + obj.cantidad_rango_4
		alimentos_encuesta = AlimentoEncuesta.objects.filter(encuesta=obj)
		# Variables nutricionales
		ref_hidratos = 0
		ref_proteinas = 0
		ref_grasasSaturadas = 0
		ref_grasasTotales = 0
		ref_kilocalorias = 0
		ref_sodio = 0
		print("Ingresando al save")
		for alimento_encuesta in alimentos_encuesta:
			print("Ingresando al alimento en save")
			ref_alimento = Alimento.objects.get(id=alimento_encuesta.alimento.id)
			print(ref_alimento.hidratos_carbono)
			print(type(ref_alimento))
			porcion = alimento_encuesta.cantidad/raciones
			print("Calculo porcion")
			print(porcion)
			ref_hidratos += alimento_encuesta.alimento.hidratos_carbono * porcion / ref_alimento.cantidad_porcion
			ref_proteinas += alimento_encuesta.alimento.proteinas * porcion / ref_alimento.cantidad_porcion
			print("Calculo proteinas" + alimento_encuesta.alimento.nombre)
			print(porcion)
			ref_grasasSaturadas += alimento_encuesta.alimento.grasas * porcion / ref_alimento.cantidad_porcion
			ref_grasasTotales += alimento_encuesta.alimento.grasas_totales * porcion / ref_alimento.cantidad_porcion
			ref_kilocalorias += alimento_encuesta.alimento.energia * porcion / ref_alimento.cantidad_porcion
			ref_sodio += alimento_encuesta.alimento.sodio * porcion / ref_alimento.cantidad_porcion
		

		ref_hidratos = round(ref_hidratos, 2)
		ref_proteinas = round(ref_proteinas, 2)
		ref_grasasSaturadas = round(ref_grasasSaturadas, 2)
		ref_grasasTotales = round(ref_grasasTotales, 2)
		ref_kilocalorias = round(ref_kilocalorias, 2)
		ref_sodio = round(ref_sodio, 2)

		ReporteNutricional.objects.create(comedor = obj.comedor, 
									organizacion = obj.organizacion,
									encuesta = obj,
									fecha = obj.fecha,
									porciones = raciones,
									hidratos = ref_hidratos,
    								proteinas = ref_proteinas,
    								grasasSaturadas = ref_grasasSaturadas,
    								grasasTotales = ref_grasasTotales,
    								kilocalorias = ref_kilocalorias,
    								sodio = ref_sodio
									)


admin.site.register(Encuesta, EncuestaAdmin)
admin.site.register(NoSeSirvioEncuesta)
admin.site.register(AlimentoEncuesta)
