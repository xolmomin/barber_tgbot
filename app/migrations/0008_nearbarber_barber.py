# Generated by Django 3.0.5 on 2020-04-21 08:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20200421_1318'),
    ]

    operations = [
        migrations.AddField(
            model_name='nearbarber',
            name='barber',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Barber'),
        ),
    ]