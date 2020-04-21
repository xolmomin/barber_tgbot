# Generated by Django 3.0.5 on 2020-04-21 08:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_nearbarber'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nearbarber',
            name='barber',
        ),
        migrations.AddField(
            model_name='nearbarber',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.TgUser'),
        ),
    ]
