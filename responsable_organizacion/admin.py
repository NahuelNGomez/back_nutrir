from django.contrib import admin
from .models import ResponsableOrganizacion, UsuarioPersonalizado


# Register your models here.
class ResponsableOrganizacionAdmin(admin.ModelAdmin):

    list_display = ['responsable', 'organizacion']
    search_fields = ('responsable', 'organizacion')


class ResponsableOrganizacionInline(admin.TabularInline):
    model = ResponsableOrganizacion
    can_delete = True
    
#admin.site.register(ResponsableOrganizacion, ResponsableOrganizacionAdmin)