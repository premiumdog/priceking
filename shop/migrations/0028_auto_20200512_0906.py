# Generated by Django 3.0.6 on 2020-05-12 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0027_category_category_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_banner_img',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='category',
            name='category_banner_link',
            field=models.CharField(default='', max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='category_image',
            field=models.ImageField(default='', null=True, upload_to=''),
        ),
    ]
