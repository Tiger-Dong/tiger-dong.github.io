from django.db import models

class Instrument(models.Model):
    instrument_name = models.CharField(max_length=100)
    parameter = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.instrument_name} - {self.parameter}"