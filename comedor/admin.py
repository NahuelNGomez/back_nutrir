from django.contrib import admin
from .forms import ComedorAdminForm
from .models import Comedor, FuncionamientoComedor#, OtrasActividadesComedor
from responsable_organizacion.models import ResponsableOrganizacion

class FuncionamientoComedorInline(admin.TabularInline):
    model = FuncionamientoComedor
    can_delete = True

#class OtrasActividadesComedorInline(admin.TabularInline):
#    model = OtrasActividadesComedor
#    can_delete = True

class ComedorAdmin(admin.ModelAdmin):

	list_display = ['nombre', 'servicio_comedor', 'organizacion_regional', 'provincia', ]
	search_fields = ('nombre', 'servicio_comedor', 'organizacion_regional', 'provincia',)
	list_filter = ('provincia', 'organizacion_regional', 'asistentes_diarios', 'servicio_comedor')

	fieldsets = (
	  ('Datos Generales', {
		  'fields': ('nombre', 'servicio_comedor', 'activo', 'organizacion_regional')
	  }),
	  ('Ubicación', {
		  'fields': ('provincia', 'departamento', 'gobierno_local', 'localidad', 'barrio', 'calle', 'numero', 'entre_calles', 'ubicacion_georreferencial', 'latitud', 'longitud')
	  }),
	  ('Actividades', {
		  'fields': ('fecha_inicio_actividad', 'descripcion', 'actividades', )
	  }),
	  ('Espacio', {
		  'fields': ('cantidad_trabajadores', 'asistentes_diarios', 'tipos_energia', 'fuente_agua', 'fuente_agua_potable',  )
	  }),
	   ('Responsable', {
		  'fields': ('responsable_comedor', )
	  }),
	)
	inlines = [FuncionamientoComedorInline]
	form = ComedorAdminForm

	def get_queryset(self, request):
		qs = super(ComedorAdmin, self).get_queryset(request)
		if not request.user.is_superuser:
			organizaciones = ResponsableOrganizacion.objects.filter(responsable=request.user).values('organizacion')
			comedores = Comedor.objects.filter(organizacion_regional__in=organizaciones)
			qs = qs.filter(id__in=comedores).distinct()
		return qs

	def filter_model_queryset_by_user(self, user, model):

		if user.is_superuser:
			return model.objects.all()

		model_name = model._meta.model_name

		if model_name == 'organizacion':
			organizacion_ids = ResponsableOrganizacion.objects.filter(responsable=user.id).values('organizacion')
			return model.objects.filter(id__in=organizacion_ids).distinct()

		return model.objects.all()

	def formfield_for_foreignkey(self, db_field, request, **kwargs):

		if request.user.is_superuser:
			return super().formfield_for_foreignkey(db_field, request, **kwargs)

		kwargs['queryset'] = self.filter_model_queryset_by_user(
			request.user, db_field.remote_field.model
		)
		return super().formfield_for_foreignkey(db_field, request, **kwargs)

class FuncionamientoComedorAdmin(admin.ModelAdmin):

    list_display = ['comedor', 'dia', 'funcionamiento', ]
    search_fields = ('comedor', 'dia', 'funcionamiento',)

#class OtrasActividadesComedorAdmin(admin.ModelAdmin):

#    list_display = ['comedor', 'descripcion', ]
#    search_fields = ('comedor', 'descripcion', )

admin.site.register(Comedor, ComedorAdmin)
#admin.site.register(FuncionamientoComedor, FuncionamientoComedorAdmin)
#admin.site.register(OtrasActividadesComedor, OtrasActividadesComedorAdmin)
