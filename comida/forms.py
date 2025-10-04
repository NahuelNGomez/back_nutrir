from django import forms
from django.core.exceptions import ValidationError
from .models import Alimento, Comida, Horario

class AlimentoForm(forms.ModelForm):

	class Meta:
		model = Alimento
		fields = '__all__'

	def clean(self):
		cleaned_data = super().clean()
		if not self.cleaned_data.get('alimento'):
			raise ValidationError('La comida tiene que tener al menos un alimento')
		return cleaned_data

class ComidaForm(forms.ModelForm):
    horarios = forms.ModelMultipleChoiceField(
        queryset=Horario.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Horarios a servir',
        help_text='Selecciona uno o más horarios para esta comida'
    )

    class Meta:
        model = Comida
        fields = ['nombre', 'foto', 'alimento', 'horarios']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer que el widget de horarios sea más amigable
        self.fields['horarios'].widget.attrs.update({'class': 'form-check-input'})
