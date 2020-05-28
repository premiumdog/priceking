# Generated by Django 3.0.3 on 2020-04-23 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20200423_1036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_category',
            field=models.CharField(choices=[('Nedves kutyatáp', 'Nedves kutyatáp'), ('Kutyaház', 'Kutyaház'), ('Kutyaszállító box, Utazás', 'Kutyaszállító box, Utazás'), ('Jutalomfalat & snack', 'Jutalomfalat & snack'), ('Kutyafekhely', 'Kutyafekhely'), ('Kutya ápolás, szőrnyírás', 'Kutya ápolás, szőrnyírás'), ('Speciális eledelek, táplálékkiegészítők', 'Speciális eledelek, táplálékkiegészítők'), ('Kutya játékok', 'Kutya játékok'), ('Pórázok, nyakörvek', 'Pórázok, nyakörvek'), ('Kutyatál, Kutya itató', 'Kutyatál, Kutya itató'), ('Sport & kiképzés', 'Sport & kiképzés'), ('Kutyaruha', 'Kutyaruha'), ('Kutyaeledel méret & fajta szerint', 'Kutyaeledel méret & fajta szerint'), ('Kölyökkutya', 'Kölyökkutya'), ('Kutyakozmetikai termékek', 'Kutyakozmetikai termékek')], max_length=254, null=True),
        ),
    ]
