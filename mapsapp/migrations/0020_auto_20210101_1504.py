# Generated by Django 3.1.4 on 2021-01-01 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapsapp', '0019_auto_20200401_2003'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='mod_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='rms',
            name='mod_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
