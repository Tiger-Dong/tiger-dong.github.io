# A料 与 B料 的 数据显示 

from django import forms
from django.forms import inlineformset_factory
from .models import Job, Chemical_A
    

# 使 B料 除投入份数外可写入外，其余皆为 只读
class JobForm(forms.ModelForm):
    theory_shares_ratio = forms.DecimalField(initial=0,
        widget=forms.TextInput(attrs={'readonly':'readonly'}))
    chemical_B_NCO = forms.DecimalField(initial=Job.chemicalData_B["nco"],
        widget=forms.TextInput(attrs={'readonly':'readonly'}))
    chemical_B_functionality = forms.IntegerField(initial=Job.chemicalData_B["functionality"],
        widget=forms.NumberInput(attrs={'readonly':'readonly'})) 
    chemical_B_molecular_mass = forms.IntegerField(initial=Job.chemicalData_B["molecule_quality"],
        widget=forms.NumberInput(attrs={'readonly':'readonly'})) 
    class Meta:
        model = Job
        exclude = ['N0', 'N1', 'N2', 'N3', 'N4', 'N5', 'sbatch_job_id', 'status']
        fields = '__all__'
        
# 使 A料 除投入份数外可写入外，其余皆为 只读
class Chemical_AForm(forms.ModelForm):
    name = forms.ChoiceField(choices=Chemical_A.CHEMICAL_A_CHOICES)
    functionality = forms.IntegerField(widget=forms.NumberInput(attrs={'readonly':'readonly'})) 
    hydroxyl = forms.DecimalField(widget=forms.NumberInput(attrs={'readonly':'readonly'})) 
    molecular_mass = forms.IntegerField(widget=forms.NumberInput(attrs={'readonly':'readonly'}))
    class Meta:
        model = Chemical_A
        fields = '__all__'
    
    
# 定义 A料 表格 行的数量，并设置不可改变
Chemical_AFormSet = inlineformset_factory(Job, Chemical_A, form=Chemical_AForm, extra=9, 
                                          max_num=9, can_delete=False)