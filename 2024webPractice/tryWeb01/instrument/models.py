from django.db import models

class Instrument(models.Model):
    name = models.CharField(max_length=100)
    parameter = models.TextField()

    def __str__(self):
        return self.name