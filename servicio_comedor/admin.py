from django.contrib import admin
from .models import ServicioComedor

# Register your models here.
class ServicioComedorAdmin(admin.ModelAdmin):

    list_display = ['nombre']
    search_fields = ('nombre',)

admin.site.register(ServicioComedor, ServicioComedorAdmin)