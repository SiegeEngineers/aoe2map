# Generated by Django 4.0.1 on 2022-01-09 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapsapp', '0020_auto_20210101_1504'),
    ]

    @staticmethod
    def calculate_id(rms_uuid, rms_model):
        uuid_str = str(rms_uuid)
        for strlen in range(6, len(uuid_str)-1):
            candidate = uuid_str[:strlen]
            if not rms_model.objects.filter(id=candidate):
                return candidate

    def calculate_defaults(apps, schema_editor):
        Rms = apps.get_model('mapsapp', 'Rms')
        for rms in Rms.objects.all().iterator():
            rms.id = Migration.calculate_id(rms.uuid, Rms)
            rms.save()

    operations = [
        migrations.AddField(
            model_name='rms',
            name='id',
            field=models.CharField(null=True, max_length=255),
        ),
        migrations.RunPython(calculate_defaults, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='rms',
            name='id',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
