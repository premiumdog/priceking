# Generated by Django 3.0.3 on 2020-04-27 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_auto_20200427_1235'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_visitor',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]