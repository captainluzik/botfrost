# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-13 11:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0013_auto_20161013_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='balance',
            field=models.FloatField(verbose_name='Баланс'),
        ),
    ]
