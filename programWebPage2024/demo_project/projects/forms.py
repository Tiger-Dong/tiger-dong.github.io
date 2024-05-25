from django import forms
from .models import Project, ProjectStage

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['Name', 'LoB', "Site", "DRI", "Creator", "Description"]
        
class ProjectStageForm(forms.ModelForm):
    State = forms.ChoiceField(choices=ProjectStage.STATE_CHOICES)
    class Meta:
        model = ProjectStage
        fields = ['State', 'project']        