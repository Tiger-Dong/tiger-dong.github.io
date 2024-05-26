from django import forms
from django.forms import inlineformset_factory
from .models import Job, Chemical_A

class JobForm(forms.ModelForm):    
    class Meta:
        model = Job
        fields = '__all__'
        
class Chemical_AForm(forms.ModelForm):
    name = forms.ChoiceField(choices=Chemical_A.CHEMICAL_A_CHOICES)
    class Meta:
        model = Chemical_A
        fields = '__all__'
    
    def complete(self):
        self.cleaned_data['functionality'] = Chemical_A.chemicalData_A[self.cleaned_data.get('name')]["functionality"]
        self.hydroxyl = Chemical_A.chemicalData_A[self.name]["hydroxyl_value"]
        self.molecular_mass = Chemical_A.chemicalData_A[self.name]["molecule_quality"]                
        return 
Chemical_AFormSet = inlineformset_factory(Job, Chemical_A, form=Chemical_AForm, extra=9, 
                                          max_num=9, can_delete=False)