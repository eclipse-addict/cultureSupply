# Generated by Django 3.2.12 on 2022-11-18 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20221118_1951'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kicks',
            name='styleId',
        ),
        migrations.AlterField(
            model_name='kicks',
            name='sku',
            field=models.CharField(max_length=100),
        ),
    ]
