# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-13 10:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0008_auto_20161013_1247'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='enter',
            options={'verbose_name': 'Пополнения счета', 'verbose_name_plural': 'Пополнение счета'},
        ),
        migrations.AlterModelOptions(
            name='paysystems',
            options={'verbose_name': 'Платежные системы', 'verbose_name_plural': 'Платежные системы'},
        ),
        migrations.AlterModelOptions(
            name='users',
            options={'verbose_name': 'Список пользователей', 'verbose_name_plural': 'Список пользователей'},
        ),
    ]