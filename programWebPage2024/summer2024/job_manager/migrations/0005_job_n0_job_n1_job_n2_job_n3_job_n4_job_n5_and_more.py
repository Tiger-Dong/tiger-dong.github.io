# Generated by Django 4.2.13 on 2024-06-05 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_manager', '0004_remove_job_chemical_b_shares_job_chemical_b_mass_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='N0',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='N1',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='N2',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='N3',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='N4',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='N5',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='sbatch_job_id',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
