# Generated by Django 3.0.5 on 2020-04-21 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_nearbarber_barber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tguser',
            name='latitude',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='tguser',
            name='longitude',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
