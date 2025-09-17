from django import forms
from .models import Area, Oficina, SalonClase, Persona

class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['nombre']

class OficinaForm(forms.ModelForm):
    class Meta:
        model = Oficina
        fields = ['codigo', 'area']

class SalonClaseForm(forms.ModelForm):
    class Meta:
        model = SalonClase
        fields = ['codigo']

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['documento', 'nombre', 'tipo', 'tipo_profesor', 'area', 'oficina']
    
    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        tipo_profesor = cleaned_data.get('tipo_profesor')
        
        if tipo == 'profesor' and not tipo_profesor:
            raise forms.ValidationError('Debe especificar el tipo de profesor.')
        return cleaned_data