# Generated by Django 5.0.4 on 2024-05-17 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inmuebles',
            name='imagen',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
