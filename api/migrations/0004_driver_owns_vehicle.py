# Generated by Django 3.0.4 on 2020-03-08 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20200308_1631'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='owns_vehicle',
            field=models.BooleanField(default=False, verbose_name='Possui veículo'),
        ),
    ]
