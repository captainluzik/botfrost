# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-13 11:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0014_auto_20161013_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enter',
            name='en_sum',
            field=models.FloatField(verbose_name='Сума пополнения'),
        ),
    ]
