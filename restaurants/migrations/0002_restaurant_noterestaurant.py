# Generated by Django 5.0.1 on 2024-05-12 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='noteRestaurant',
            field=models.FloatField(null=True),
        ),
    ]
