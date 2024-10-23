from django import forms
from dal import autocomplete
from provincia.models import Provincia
from departamento.models import Departamento
from gobierno_local.models import GobiernoLocal
from localidad.models import Localidad
from .models import Comedor, AsistentesDiariosComedor, CantidadTrabajadoresComedor
from utils.functions import Position, IntegerField
from django.db.models.functions import Cast, Substr


class ComedorAdminForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		posicion_guion = Position('rango', expression="'-'")
		
		self.fields['asistentes_diarios'].queryset = AsistentesDiariosComedor.objects.annotate(
			valor_inicial=Cast(Substr('rango', 1, posicion_guion-1), IntegerField())
        ).order_by('valor_inicial')

		self.fields['cantidad_trabajadores'].queryset = CantidadTrabajadoresComedor.objects.annotate(
            valor_inicial=Cast(Substr('rango', 1, posicion_guion-1), IntegerField())
        ).order_by('valor_inicial')

	"""Form para que en comedor se pueda buscar las localidades, los gobiernos locales
		y los departamenos en cascada"""

	provincia = forms.ModelChoiceField(
		queryset=Provincia.objects.all(),
		widget=autocomplete.ModelSelect2(url='provincia-autocomplete')
	)
	departamento = forms.ModelChoiceField(
		queryset=Departamento.objects.all(),
		widget=autocomplete.ModelSelect2(url='departamento-autocomplete', forward=('provincia',)),
		blank=True,
		required=False
	)
	gobierno_local = forms.ModelChoiceField(
		queryset=GobiernoLocal.objects.all(),
		widget=autocomplete.ModelSelect2(url='gobiernoLocal-autocomplete', forward=('departamento',)),
		blank=True,
		required=False
	)
	localidad = forms.ModelChoiceField(
		queryset=Localidad.objects.all(),
		widget=autocomplete.ModelSelect2(url='localidad-autocomplete', forward=('gobierno_local',)),
		blank=True,
		required=False
	)


