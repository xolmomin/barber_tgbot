# Generated by Django 3.0.5 on 2020-04-21 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20200421_2011'),
    ]

    operations = [
        migrations.AddField(
            model_name='tguser',
            name='check',
            field=models.BooleanField(default=False),
        ),
    ]
