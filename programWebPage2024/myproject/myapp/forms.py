from django import forms

class MaterialForm(forms.Form):
    resource_name = forms.CharField()
    functionality = forms.IntegerField()
    hydroxyl_value = forms.FloatField(required=False)
    molecule_quality = forms.FloatField()
    batch_amount = forms.FloatField()