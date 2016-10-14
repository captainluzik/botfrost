# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-13 09:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_users_date_reg'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaySystems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ps_name', models.CharField(max_length=50, verbose_name='Платежная система')),
                ('ps_abbr', models.CharField(max_length=10, verbose_name='Аббревиатура')),
                ('ps_purse', models.CharField(max_length=30, verbose_name='Счет')),
            ],
            options={
                'verbose_name': 'Платежные системы',
            },
        ),
        migrations.AlterModelOptions(
            name='users',
            options={'verbose_name': 'Список пользователей'},
        ),
    ]