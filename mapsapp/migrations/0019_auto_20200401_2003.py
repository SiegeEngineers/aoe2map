# Generated by Django 2.2.12 on 2020-04-01 20:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapsapp', '0018_collection_rms'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rms',
            options={'ordering': ['-updated']},
        ),
    ]
