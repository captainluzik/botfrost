# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-12 09:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, verbose_name='Имя пользователя')),
                ('id_user', models.IntegerField(verbose_name='ID-пользователя')),
                ('balance', models.IntegerField(verbose_name='Баланс')),
            ],
        ),
    ]
