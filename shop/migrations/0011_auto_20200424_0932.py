# Generated by Django 3.0.3 on 2020-04-24 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_auto_20200424_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]