# Generated by Django 3.0.6 on 2020-05-12 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0024_category_category_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_order',
            field=models.IntegerField(blank=True),
        ),
    ]