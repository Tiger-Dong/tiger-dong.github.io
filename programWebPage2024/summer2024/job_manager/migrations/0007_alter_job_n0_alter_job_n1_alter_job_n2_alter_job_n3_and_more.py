# Generated by Django 5.0.6 on 2024-06-09 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_manager', '0006_job_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='N0',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='N1',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='N2',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='N3',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='N4',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='N5',
            field=models.IntegerField(null=True),
        ),
    ]
