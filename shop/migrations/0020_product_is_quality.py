# Generated by Django 3.0.3 on 2020-05-06 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0019_auto_20200504_0817'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_quality',
            field=models.BooleanField(default=False),
        ),
    ]