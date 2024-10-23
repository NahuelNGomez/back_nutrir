from django.contrib import admin

from .forms import AlimentoForm
from .models import Comida
from django.utils.html import format_html

# Register your models here.
class ComidaAdmin(admin.ModelAdmin):

	def foto_tag(self, obj):
		return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.foto.url))

	list_display = ['nombre', 'foto_tag', ]
	search_fields = ('nombre',)
	form = AlimentoForm
	list_filter = ('horario',)
	ordering = ['nombre']

admin.site.register(Comida, ComidaAdmin)
