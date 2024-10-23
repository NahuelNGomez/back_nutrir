from django.contrib import admin
from .models import Organizacion
from responsable_organizacion.models import ResponsableOrganizacion

# Register your models here.

class ResponsableOrganizacionInline(admin.TabularInline):
    model = ResponsableOrganizacion
    can_delete = True

class OrganizacionAdmin(admin.ModelAdmin):
    
    list_display = ['nombre',]
    search_fields = ('nombre',)
    inlines = [ResponsableOrganizacionInline]

    def get_queryset(self, request):
        qs = super(OrganizacionAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            organizaciones = ResponsableOrganizacion.objects.filter(responsable=request.user).values('organizacion')
            qs = qs.filter(id__in=organizaciones).distinct()
        return qs
              

admin.site.register(Organizacion, OrganizacionAdmin)