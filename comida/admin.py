from django.contrib import admin

from .forms import AlimentoForm, ComidaForm
from .models import Comida, Horario
from django.utils.html import format_html

# Register your models here.
class ComidaAdmin(admin.ModelAdmin):

	def foto_tag(self, obj):
		return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.foto.url))

	def horarios_display(self, obj):
		return ", ".join([horario.nombre for horario in obj.horarios.all()])
	horarios_display.short_description = 'Horarios'

	list_display = ['nombre', 'foto_tag', 'horarios_display']
	search_fields = ('nombre',)
	form = ComidaForm
	list_filter = ('horarios',)
	ordering = ['nombre']
	filter_horizontal = ('horarios', 'alimento')

class HorarioAdmin(admin.ModelAdmin):
	list_display = ['codigo', 'nombre']
	search_fields = ('codigo', 'nombre')
	ordering = ['codigo']

admin.site.register(Comida, ComidaAdmin)
admin.site.register(Horario, HorarioAdmin)
