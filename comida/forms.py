from django import forms
from django.core.exceptions import ValidationError
from .models import Alimento

class AlimentoForm(forms.ModelForm):

	class Meta:
		model = Alimento
		fields = '__all__'

	def clean(self):
		cleaned_data = super().clean()
		if not self.cleaned_data.get('alimento'):
			raise ValidationError('La comida tiene que tener al menos un alimento')
		return cleaned_data
