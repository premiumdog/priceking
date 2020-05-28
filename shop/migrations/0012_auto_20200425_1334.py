# Generated by Django 3.0.3 on 2020-04-25 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_auto_20200424_0932'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='product_sale_price',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='product_sku',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]