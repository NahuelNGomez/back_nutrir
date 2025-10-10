# admin.py
from django.contrib import admin
from .models import Alimento, Unidad
from .models import AlimentoSARA
from django import forms
from django.utils.html import format_html
from django.utils.safestring import mark_safe
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
    
    # Nutrientes básicos
    agua = forms.DecimalField(
        label=mark_safe("<strong>Agua</strong>"),
        help_text="Por porción de 100 gramos (g)",
        widget=forms.TextInput(attrs={
            'step': '0.01',
            'min': '0',
            'class': 'nutrient-field',
            'type': 'number'
        })
    )
    
    energia = forms.DecimalField(
        label=mark_safe("<strong>Kilocalorías</strong>"),
        help_text="Por porción de 100 gramos (kcal)",
        widget=forms.TextInput(attrs={
            'step': '0.01',
            'min': '0',
            'class': 'nutrient-field',
            'type': 'number'
        })
    )
    
    proteinas = forms.DecimalField(
        label=mark_safe("<strong>Proteínas</strong>"),
        help_text="Por porción de 100 gramos (g)",
        widget=forms.TextInput(attrs={
            'step': '0.01',
            'min': '0',
            'class': 'nutrient-field',
            'type': 'number',
        })
    )
    
    lipidos = forms.DecimalField(
        label=mark_safe("<strong>Lípidos</strong>"),
        help_text="Por porción de 100 gramos (g)",
        widget=forms.TextInput(attrs={
            'step': '0.01',
            'min': '0',
            'class': 'nutrient-field',
            'type': 'number'
        })
    )
    
    # Ácidos grasos
    acidos_grasos_saturados = forms.DecimalField(
        label=mark_safe("<strong>Ácidos Grasos Saturados</strong>"),
        help_text="Por porción de 100 gramos (g)",
        widget=forms.TextInput(attrs={
            'step': '0.01',
            'min': '0',
            'class': 'nutrient-field',
            'type': 'number'
        })
    )
    
    acidos_grasos_monoinsaturados = forms.DecimalField(
        label=mark_safe("<strong>Ácidos Grasos Monoinsaturados</strong>"),
        help_text="Por porción de 100 gramos (g)",
        widget=forms.TextInput(attrs={
            'step': '0.01',
            'min': '0',
            'class': 'nutrient-field',
            'type': 'number'
        })
    )
    
    acidos_grasos_poliinsaturados = forms.DecimalField(
        label=mark_safe("<strong>Ácidos Grasos Poliinsaturados</strong>"),
        help_text="Por porción de 100 gramos (g)",
        widget=forms.TextInput(attrs={
            'step': '0.01',
            'min': '0',
            'class': 'nutrient-field',
            'type': 'number'
        })
    )
    
    colesterol = forms.DecimalField(
        label=mark_safe("<strong>Colesterol</strong>"),
        help_text="Por porción de 100 gramos (mg)",
        widget=forms.TextInput(attrs={
            'step': '0.01',
            'min': '0',
            'class': 'nutrient-field',
            'type': 'number'
        })
    )
    
    # Carbohidratos y fibra
    hidratos_carbono = forms.DecimalField(
        label=mark_safe("<strong>Hidratos de Carbono</strong>"),
        help_text="Por porción de 100 gramos (g)",
        widget=forms.TextInput(attrs={
            'step': '0.01',
            'min': '0',
            'class': 'nutrient-field',
            'type': 'number'
        })
    )
    
    fibra = forms.DecimalField(
        label=mark_safe("<strong>Fibra</strong>"),
        help_text="Por porción de 100 gramos (g)",
        widget=forms.TextInput(attrs={
            'step': '0.01',
            'min': '0',
            'class': 'nutrient-field',
            'type': 'number'
        })
    )
    
    cenizas = forms.DecimalField(
        label=mark_safe("<strong>Cenizas</strong>"),
        help_text="Por porción de 100 gramos (g)",
        widget=forms.TextInput(attrs={
            'step': '0.01',
            'min': '0',
            'class': 'nutrient-field',
            'type': 'number'
        })
    )
    
    # Minerales
    sodio = forms.DecimalField(
        label=mark_safe("<strong>Sodio</strong>"),
        help_text="Por porción de 100 gramos (mg)",
        widget=forms.TextInput(attrs={
            'step': '0.01',
            'min': '0',
            'class': 'nutrient-field',
            'type': 'number'
        })
    )
    
    potasio = forms.DecimalField(
        label=mark_safe("<strong>Potasio</strong>"),
        help_text="Por porción de 100 gramos (mg)",
        widget=forms.TextInput(attrs={
            'step': '0.01',
            'min': '0',
            'class': 'nutrient-field',
            'type': 'number'
        })
    )
    
    calcio = forms.DecimalField(
        label=mark_safe("<strong>Calcio</strong>"),
        help_text="Por porción de 100 gramos (mg)",
        widget=forms.TextInput(attrs={
            'step': '0.01',
            'min': '0',
            'class': 'nutrient-field',
            'type': 'number'
        })
    )
    
    fosforo = forms.DecimalField(
        label=mark_safe("<strong>Fósforo</strong>"),
        help_text="Por porción de 100 gramos (mg)",
        widget=forms.TextInput(attrs={
            'step': '0.01',
            'min': '0',
            'class': 'nutrient-field',
            'type': 'number'
        })
    )
    
    hierro = forms.DecimalField(
        label=mark_safe("<strong>Hierro</strong>"),
        help_text="Por porción de 100 gramos (mg)",
        widget=forms.TextInput(attrs={
            'step': '0.01',
            'min': '0',
            'class': 'nutrient-field',
            'type': 'number'
        })
    )
    
    zinc = forms.DecimalField(
        label=mark_safe("<strong>Zinc</strong>"),
        help_text="Por porción de 100 gramos (mg)",
        widget=forms.TextInput(attrs={
            'step': '0.01',
            'min': '0',
            'class': 'nutrient-field',
            'type': 'number'
        })
    )
    
    # Vitaminas
    niacina = forms.DecimalField(
        label=mark_safe("<strong>Niacina</strong>"),
        help_text="Por porción de 100 gramos (mg)",
        widget=forms.TextInput(attrs={
            'step': '0.01',
            'min': '0',
            'class': 'nutrient-field',
            'type': 'number'
        })
    )
    
    folatos = forms.DecimalField(
        label=mark_safe("<strong>Folatos</strong>"),
        help_text="Por porción de 100 gramos (μg)",
        widget=forms.TextInput(attrs={
            'step': '0.01',
            'min': '0',
            'class': 'nutrient-field',
            'type': 'number'
        })
    )
    
    vitamina_a = forms.DecimalField(
        label=mark_safe("<strong>Vitamina A</strong>"),
        help_text="Por porción de 100 gramos (μg RAE)",
        widget=forms.TextInput(attrs={
            'step': '0.01',
            'min': '0',
            'class': 'nutrient-field',
            'type': 'number'
        })
    )
    
    tiamina = forms.DecimalField(
        label=mark_safe("<strong>Tiamina (B1)</strong>"),
        help_text="Por porción de 100 gramos (mg)",
        widget=forms.TextInput(attrs={
            'step': '0.01',
            'min': '0',
            'class': 'nutrient-field',
            'type': 'number'
        })
    )
    
    riboflavina = forms.DecimalField(
        label=mark_safe("<strong>Riboflavina (B2)</strong>"),
        help_text="Por porción de 100 gramos (mg)",
        widget=forms.TextInput(attrs={
            'step': '0.01',
            'min': '0',
            'class': 'nutrient-field',
            'type': 'number'
        })
    )
    
    vitamina_b12 = forms.DecimalField(
        label=mark_safe("<strong>Vitamina B12</strong>"),
        help_text="Por porción de 100 gramos (μg)",
        widget=forms.TextInput(attrs={
            'step': '0.01',
            'min': '0',
            'class': 'nutrient-field',
            'type': 'number'
        })
    )
    
    vitamina_c = forms.DecimalField(
        label=mark_safe("<strong>Vitamina C</strong>"),
        help_text="Por porción de 100 gramos (mg)",
        widget=forms.TextInput(attrs={
            'step': '0.01',
            'min': '0',
            'class': 'nutrient-field',
            'type': 'number'
        })
    )
    
    vitamina_d = forms.DecimalField(
        label=mark_safe("<strong>Vitamina D</strong>"),
        help_text="Por porción de 100 gramos (UI)",
        widget=forms.TextInput(attrs={
            'step': '0.01',
            'min': '0',
            'class': 'nutrient-field',
            'type': 'number'
        })
    )
    
    # Campos legacy para compatibilidad
    grasas = forms.DecimalField(
        label=mark_safe("<strong>Grasas Saturadas</strong>"),
        help_text="Por porción de 100 gramos (g) - usar acidos_grasos_saturados",
        required=False,
        widget=forms.TextInput(attrs={
            'step': '0.01',
            'min': '0',
            'class': 'nutrient-field',
            'type': 'number',
            'data-localization': 'false',
            'style': 'text-align: right;'
        })
    )
    
    grasas_totales = forms.DecimalField(
        label=mark_safe("<strong>Grasas Totales</strong>"),
        help_text="Por porción de 100 gramos (g) - usar lipidos",
        required=False,
        widget=forms.TextInput(attrs={
            'step': '0.01',
            'min': '0',
            'class': 'nutrient-field',
            'type': 'number'
        })
    )

    class Meta:
        model = Alimento
        fields = [
            'alimento_sara', 'foto', 'nombre', 'cantidad_porcion', 'unidades',
            # Nutrientes básicos
            'agua', 'energia', 'proteinas', 'lipidos',
            # Ácidos grasos
            'acidos_grasos_saturados', 'acidos_grasos_monoinsaturados', 'acidos_grasos_poliinsaturados', 'colesterol',
            # Carbohidratos y fibra
            'hidratos_carbono', 'fibra', 'cenizas',
            # Minerales
            'sodio', 'potasio', 'calcio', 'fosforo', 'hierro', 'zinc',
            # Vitaminas
            'niacina', 'folatos', 'vitamina_a', 'tiamina', 'riboflavina', 'vitamina_b12', 'vitamina_c', 'vitamina_d',
            # Campos legacy
            'grasas', 'grasas_totales'
        ]
    class Media:
        js = (
            'admin/js/vendor/select2/select2.full.min.js',
            'admin/js/fill_alimento_fields.js',
            'admin/js/remove_g_indicators.js',
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
        
        # Inicialmente, solo el nombre es requerido
        self.fields['nombre'].required = True
        self.fields['cantidad_porcion'].required = False
        
        # Los campos de nutrientes no son requeridos (pueden ser 0)
        nutrient_fields = [
            'agua', 'energia', 'proteinas', 'lipidos',
            'acidos_grasos_saturados', 'acidos_grasos_monoinsaturados', 'acidos_grasos_poliinsaturados', 'colesterol',
            'hidratos_carbono', 'fibra', 'cenizas', 'sodio', 'potasio', 'calcio', 'fosforo', 'hierro', 'zinc',
            'niacina', 'folatos', 'vitamina_a', 'tiamina', 'riboflavina', 'vitamina_b12', 'vitamina_c', 'vitamina_d'
        ]
        for field in nutrient_fields:
            self.fields[field].required = False
                
    def clean(self):
        cleaned_data = super().clean()
        alimento_sara = cleaned_data.get('alimento_sara')
                
        # Si se ha seleccionado un alimento de la tabla SARA, se completan los campos automaticamente
        if alimento_sara:
            cleaned_data['nombre'] = alimento_sara.nombre
            cleaned_data['cantidad_porcion'] = alimento_sara.cantidad_porcion
            # Mapear campos de SARA a los nuevos campos del modelo
            cleaned_data['agua'] = getattr(alimento_sara, 'agua', 0)
            cleaned_data['energia'] = alimento_sara.energia
            cleaned_data['proteinas'] = alimento_sara.proteinas
            cleaned_data['lipidos'] = getattr(alimento_sara, 'lipidos', alimento_sara.grasas_totales)
            cleaned_data['acidos_grasos_saturados'] = getattr(alimento_sara, 'acidos_grasos_saturados', alimento_sara.grasas)
            cleaned_data['acidos_grasos_monoinsaturados'] = getattr(alimento_sara, 'acidos_grasos_monoinsaturados', 0)
            cleaned_data['acidos_grasos_poliinsaturados'] = getattr(alimento_sara, 'acidos_grasos_poliinsaturados', 0)
            cleaned_data['colesterol'] = getattr(alimento_sara, 'colesterol', 0)
            cleaned_data['hidratos_carbono'] = alimento_sara.hidratos_carbono
            cleaned_data['fibra'] = getattr(alimento_sara, 'fibra', 0)
            cleaned_data['cenizas'] = getattr(alimento_sara, 'cenizas', 0)
            cleaned_data['sodio'] = alimento_sara.sodio
            cleaned_data['potasio'] = getattr(alimento_sara, 'potasio', 0)
            cleaned_data['calcio'] = getattr(alimento_sara, 'calcio', 0)
            cleaned_data['fosforo'] = getattr(alimento_sara, 'fosforo', 0)
            cleaned_data['hierro'] = getattr(alimento_sara, 'hierro', 0)
            cleaned_data['zinc'] = getattr(alimento_sara, 'zinc', 0)
            cleaned_data['niacina'] = getattr(alimento_sara, 'niacina', 0)
            cleaned_data['folatos'] = getattr(alimento_sara, 'folatos', 0)
            cleaned_data['vitamina_a'] = getattr(alimento_sara, 'vitamina_a', 0)
            cleaned_data['tiamina'] = getattr(alimento_sara, 'tiamina', 0)
            cleaned_data['riboflavina'] = getattr(alimento_sara, 'riboflavina', 0)
            cleaned_data['vitamina_b12'] = getattr(alimento_sara, 'vitamina_b12', 0)
            cleaned_data['vitamina_c'] = getattr(alimento_sara, 'vitamina_c', 0)
            cleaned_data['vitamina_d'] = getattr(alimento_sara, 'vitamina_d', 0)
            
		# Si no se seleccionó un alimento de la tabla SARA, solo se requiere el nombre
        else:
            # Solo el nombre es requerido, los nutrientes pueden ser 0
            if not cleaned_data.get('nombre'):
                self.add_error('nombre', 'El nombre del alimento es requerido.')
            
            # Establecer valores por defecto de 0 para nutrientes vacíos
            nutrient_fields = [
                'agua', 'energia', 'proteinas', 'lipidos',
                'acidos_grasos_saturados', 'acidos_grasos_monoinsaturados', 'acidos_grasos_poliinsaturados', 'colesterol',
                'hidratos_carbono', 'fibra', 'cenizas', 'sodio', 'potasio', 'calcio', 'fosforo', 'hierro', 'zinc',
                'niacina', 'folatos', 'vitamina_a', 'tiamina', 'riboflavina', 'vitamina_b12', 'vitamina_c', 'vitamina_d'
            ]
            
            for field in nutrient_fields:
                if not cleaned_data.get(field):
                    cleaned_data[field] = 0

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
    list_display = ['nombre', 'cantidad_porcion', 'energia', 'proteinas', 'lipidos', 'sodio']
    search_fields = ['nombre']
    list_filter = ['energia', 'proteinas', 'lipidos']
    ordering = ['nombre']
    list_per_page = 50
    list_max_show_all = 100
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'cantidad_porcion')
        }),
        ('Nutrientes Básicos', {
            'fields': ('agua', 'energia', 'proteinas', 'lipidos')
        }),
        ('Ácidos Grasos', {
            'fields': ('acidos_grasos_saturados', 'acidos_grasos_monoinsaturados', 'acidos_grasos_poliinsaturados', 'colesterol')
        }),
        ('Carbohidratos y Fibra', {
            'fields': ('hidratos_carbono', 'fibra', 'cenizas')
        }),
        ('Minerales', {
            'fields': ('sodio', 'potasio', 'calcio', 'fosforo', 'hierro', 'zinc')
        }),
        ('Vitaminas', {
            'fields': ('niacina', 'folatos', 'vitamina_a', 'tiamina', 'riboflavina', 'vitamina_b12', 'vitamina_c', 'vitamina_d')
        }),
        ('Campos Legacy', {
            'fields': ('grasas', 'grasas_totales'),
            'classes': ('collapse',)
        })
    )

admin.site.register(Alimento, AlimentoAdmin)
admin.site.register(Unidad, UnidadAdmin)
admin.site.register(AlimentoSARA, AlimentoSARAAdmin)


