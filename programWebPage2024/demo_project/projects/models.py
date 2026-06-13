from typing import Iterable
from django.db import models
from django.core.validators import EmailValidator

class Project(models.Model):
    Name = models.CharField(max_length=100, default="Sentinel 101")
    LoB = models.CharField(max_length=200)
    Site = models.CharField(max_length=200)
    DRI = models.EmailField(validators=[EmailValidator])
    Creator = models.EmailField(validators=[EmailValidator])
    Description = models.TextField()
    Created_time = models.DateTimeField(auto_now_add=True)
    Updated_time = models.DateTimeField(auto_now=True)

    # def save(self, *args, **kwargs) -> None:
        # is_new = not self.pk             
        # super().save(*args, **kwargs)
        # if is_new:
        #     ps = ProjectStage.objects.create(project=self, State='init')
        #     ps.save()
        # return 

class ProjectStage(models.Model):
    STATE_CHOICES = [
        ('init', 'Init'),
        ('data_collection', 'Data Collection'),
        ('model_training', 'Model Training'),
        ('under_deployment', 'Under Deployment'),
        ('control_run_on_production', 'Control Run On Production'),
        ('OK2ML', 'OK2ML'),
        ('Pause', 'Pause'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    Updated_time = models.DateTimeField(auto_now=True)
    State = models.CharField(max_length=30, choices=STATE_CHOICES, default='init')

    def __str__(self) -> str:
        return f'{self.State}'