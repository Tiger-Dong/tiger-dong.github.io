# Generated by Django 5.0.6 on 2024-05-24 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='Name',
            field=models.CharField(default='Sentinel 101', max_length=100),
        ),
    ]
