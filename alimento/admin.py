# admin.py
from django.contrib import admin
from .models import Alimento, Unidad
from .models import AlimentoSARA
from django import forms
from django.utils.html import format_html
from django.core.exceptions import ValidationError


class UnidadAdminForm(forms.ModelForm):
    class Meta:
        model = Unidad
        fields = ['nombre', 'equivalencia_gramos', 'equivalencia_ml']
        widgets = {
            'equivalencia_gramos': forms.NumberInput(attrs={
                'step': '0.01',
                'min': '0',
                'placeholder': 'Ej: 100.50'
            }),
            'equivalencia_ml': forms.NumberInput(attrs={
                'step': '0.01', 
                'min': '0',
                'placeholder': 'Ej: 250.00'
            })
        }
    
    def clean_equivalencia_gramos(self):
        valor = self.cleaned_data.get('equivalencia_gramos')
        if valor is not None and valor < 0:
            raise ValidationError("El valor debe ser mayor o igual a 0")
        return valor
    
    def clean_equivalencia_ml(self):
        valor = self.cleaned_data.get('equivalencia_ml')
        if valor is not None and valor < 0:
            raise ValidationError("El valor debe ser mayor o igual a 0")
        return valor


class AlimentoAdminForm(forms.ModelForm):
    # Creamos un campo de selección para elegir un alimento ya existente de la tabla SARA
    alimento_sara = forms.ModelChoiceField(
        queryset=AlimentoSARA.objects.all().order_by('nombre'),
        required=False,
        label="Seleccionar Alimento de tabla SARA",
        help_text="Seleccione un alimento para rellenar automáticamente los valores nutricionales",
        widget=forms.Select(attrs={
            'class': 'select2-widget',
            'data-placeholder': 'Buscar alimento de tabla SARA...'
        })
    )
    
    # Campos nutricionales personalizados con "G" y texto de ayuda
    hidratos_carbono = forms.DecimalField(
        label="Hidratos de Carbono",
        help_text="Por porción de 100 gramos",
        widget=forms.NumberInput(attrs={
            'step': '0.01',
            'min': '0',
            'class': 'nutrient-field'
        })
    )
    
    proteinas = forms.DecimalField(
        label="Proteínas",
        help_text="Por porción de 100 gramos",
        widget=forms.NumberInput(attrs={
            'step': '0.01',
            'min': '0',
            'class': 'nutrient-field'
        })
    )
    
    grasas = forms.DecimalField(
        label="Grasas Saturadas",
        help_text="Por porción de 100 gramos",
        widget=forms.NumberInput(attrs={
            'step': '0.01',
            'min': '0',
            'class': 'nutrient-field'
        })
    )
    
    grasas_totales = forms.DecimalField(
        label="Grasas Totales",
        help_text="Por porción de 100 gramos",
        widget=forms.NumberInput(attrs={
            'step': '0.01',
            'min': '0',
            'class': 'nutrient-field'
        })
    )
    
    energia = forms.DecimalField(
        label="Kilocalorías",
        help_text="Por porción de 100 gramos",
        widget=forms.NumberInput(attrs={
            'step': '0.01',
            'min': '0',
            'class': 'nutrient-field'
        })
    )
    
    sodio = forms.DecimalField(
        label="Sodio",
        help_text="Por porción de 100 gramos",
        widget=forms.NumberInput(attrs={
            'step': '0.01',
            'min': '0',
            'class': 'nutrient-field'
        })
    )

    class Meta:
        model = Alimento
        fields = ['alimento_sara', 'foto', 'nombre', 'cantidad_porcion', 'unidades',  # Aquí añade 'unidades'
                  'hidratos_carbono', 'proteinas', 'grasas', 'grasas_totales', 'energia', 'sodio']
    class Media:
        js = (
            'admin/js/vendor/select2/select2.full.min.js',
            'admin/js/fill_alimento_fields.js',
        )
        css = {
            'all': (
                'admin/css/vendor/select2/select2.min.css',
                'admin/css/custom_admin.css',
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['unidades'].initial = self.instance.unidades.all()
        
        # Establecer valor por defecto de 1 para cantidad_porcion
        if not self.instance.pk:  # Solo para nuevos registros
            self.fields['cantidad_porcion'].initial = 1
        
        # Inicialmente, todos los campos son NO requeridos
        for field in ['nombre', 'cantidad_porcion', 'hidratos_carbono', 'proteinas', 
                      'grasas', 'grasas_totales', 'energia', 'sodio']:
            self.fields[field].required = False
                
    def clean(self):
        cleaned_data = super().clean()
        alimento_sara = cleaned_data.get('alimento_sara')
                
        # Si se ha seleccionado un alimento de la tabla SARA, se completan los campos automaticamente
        if alimento_sara:
            # Solo completar el nombre si el usuario no lo cambió o está vacío
            if not cleaned_data.get('nombre') or cleaned_data.get('nombre') == alimento_sara.nombre:
                cleaned_data['nombre'] = alimento_sara.nombre
            
            # Completar los otros campos nutricionales solo si están vacíos (None o '')
            if cleaned_data.get('cantidad_porcion') is None or cleaned_data.get('cantidad_porcion') == '':
                cleaned_data['cantidad_porcion'] = alimento_sara.cantidad_porcion
            if cleaned_data.get('hidratos_carbono') is None or cleaned_data.get('hidratos_carbono') == '':
                cleaned_data['hidratos_carbono'] = alimento_sara.hidratos_carbono
            if cleaned_data.get('proteinas') is None or cleaned_data.get('proteinas') == '':
                cleaned_data['proteinas'] = alimento_sara.proteinas
            if cleaned_data.get('grasas') is None or cleaned_data.get('grasas') == '':
                cleaned_data['grasas'] = alimento_sara.grasas
            if cleaned_data.get('grasas_totales') is None or cleaned_data.get('grasas_totales') == '':
                cleaned_data['grasas_totales'] = alimento_sara.grasas_totales
            if cleaned_data.get('energia') is None or cleaned_data.get('energia') == '':
                cleaned_data['energia'] = alimento_sara.energia
            if cleaned_data.get('sodio') is None or cleaned_data.get('sodio') == '':
                cleaned_data['sodio'] = alimento_sara.sodio
        
        # Asegurar que los campos vacíos se guarden como 0.00
        campos_nutricionales = ['cantidad_porcion', 'hidratos_carbono', 'proteinas', 'grasas', 'grasas_totales', 'energia', 'sodio']
        for campo in campos_nutricionales:
            if cleaned_data.get(campo) is None or cleaned_data.get(campo) == '':
                cleaned_data[campo] = 0.00
            
        # Solo el nombre es requerido
        if not cleaned_data.get('nombre'):
            self.add_error('nombre', 'Este campo es requerido.')

        return cleaned_data

class AlimentoAdmin(admin.ModelAdmin):
    form = AlimentoAdminForm

    def foto_tag(self, obj):
        return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.foto.url))

    list_display = ['nombre', 'foto_tag',]
    search_fields = ('nombre',)
    ordering = ['nombre']
    
    
class UnidadAdmin(admin.ModelAdmin):
    form = UnidadAdminForm
    list_display = ['nombre', 'equivalencia_gramos', 'equivalencia_ml']
    search_fields = ['nombre']
    list_filter = ['equivalencia_gramos', 'equivalencia_ml']
    
    # Configuración para mejorar la experiencia con popups
    save_on_top = False  # Solo mostrar botones abajo
    save_as = False
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Añadir ayuda para los campos de equivalencia
        if 'equivalencia_gramos' in form.base_fields:
            form.base_fields['equivalencia_gramos'].help_text = "Equivalencia de 1 unidad en gramos (no llenar si usa ml)"
        if 'equivalencia_ml' in form.base_fields:
            form.base_fields['equivalencia_ml'].help_text = "Equivalencia de 1 unidad en ml (no llenar si usa gramos)"
        return form
    
    def response_add(self, request, obj, post_url_continue=None):
        """Manejar la respuesta después de agregar una nueva unidad"""
        if request.POST.get('_popup'):
            # Si es un popup, usar la respuesta estándar de Django
            return super().response_add(request, obj, post_url_continue)
        return super().response_add(request, obj, post_url_continue)

class AlimentoSARAAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'cantidad_porcion', 'energia', 'proteinas']
    search_fields = ['nombre']
    ordering = ['nombre']
    list_per_page = 50

admin.site.register(Alimento, AlimentoAdmin)
admin.site.register(Unidad, UnidadAdmin)
admin.site.register(AlimentoSARA, AlimentoSARAAdmin)


