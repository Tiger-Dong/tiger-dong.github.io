from django.db import models

class ChemicalMaterial(models.Model):
    name = models.CharField(max_length=100)
    functionality = models.IntegerField()
    hydroxyl_value = models.FloatField(null=True, blank=True)
    molecule_quality = models.FloatField()
    batch_amount = models.FloatField()
    nco_value = models.FloatField()
    temperature_amount  = models.FloatField(blank=False)