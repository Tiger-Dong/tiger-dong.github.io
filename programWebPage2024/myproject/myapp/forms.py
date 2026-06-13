from django import forms
from .models import ChemicalMaterial

class MaterialForm(forms.ModelForm):
    
    class Meta:
        model = ChemicalMaterial
        fields = '__all__'