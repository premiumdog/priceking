# Generated by Django 3.0.3 on 2020-04-23 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20200423_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_price',
            field=models.IntegerField(blank=True, max_length=254, null=True),
        ),
    ]