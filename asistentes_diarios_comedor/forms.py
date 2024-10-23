from django import forms

MSJ_ERROR = 'El formato debe ser "X - X"'

class AsistentesDiariosComedorAdminForm(forms.ModelForm):
    rango = forms.CharField()

    def clean_rango(self):
        rango = self.cleaned_data.get('rango')

        if len(rango.split('-')) != 2:
            raise forms.ValidationError(MSJ_ERROR)
        
        for valor in rango.split('-'):
            if not valor.strip().isnumeric():
                raise forms.ValidationError(MSJ_ERROR)
        return rango