# Generated by Django 5.0.6 on 2024-07-06 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='price',
            field=models.FloatField(default=0.0),
        ),
    ]
