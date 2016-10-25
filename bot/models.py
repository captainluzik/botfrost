from django.db import models
from datetime import datetime


class Users(models.Model):
    username = models.CharField(max_length=50, verbose_name='Имя пользователя')
    id_user = models.IntegerField(verbose_name='ID-пользователя')
    balance = models.FloatField(verbose_name='Баланс', default=0.0)
    date_reg = models.DateTimeField(verbose_name='Дата регистрации', auto_now_add=True)

    class Meta:
        verbose_name = 'Список пользователей'
        verbose_name_plural = 'Список пользователей'

    def __str__(self):
        return self.username


class PaySystems(models.Model):
    ps_name = models.CharField(max_length=50, verbose_name='Платежная система')
    ps_abbr = models.CharField(max_length=10, verbose_name='Аббревиатура')
    ps_purse = models.CharField(max_length=30, verbose_name='Счет')

    class Meta:
        verbose_name = 'Платежные системы'
        verbose_name_plural = 'Платежные системы'

    def __str__(self):
        return self.ps_name


class Enter(models.Model):
    STATUS = [
        (1, 'В ожидании'),
        (2, 'Обработано'),
        (3, 'Отменено')
    ]

    username = models.ForeignKey(Users, verbose_name='Имя пользователя')
    en_id = models.IntegerField(verbose_name='ID-транкзации')
    en_ps = models.ForeignKey(PaySystems, verbose_name='Платежная система')
    en_date = models.DateTimeField(verbose_name='Дата пополнения')
    en_sum = models.FloatField(verbose_name='Сума пополнения')
    en_status = models.IntegerField(
        verbose_name='Статус платежа',
        choices=STATUS
    )

    class Meta:
        verbose_name = 'Пополнения счета'
        verbose_name_plural = 'Пополнение счета'

    def __str__(self):
        return self.username.username


class Withdrawal(models.Model):
    STATUS = [
        (1, 'В ожидании'),
        (2, 'Обработано'),
        (3, 'Отменено')
    ]

    username = models.ForeignKey(Users, verbose_name='Имя пользователя')
    wd_id = models.IntegerField(verbose_name='ID-транкзации')
    wd_ps = models.ForeignKey(PaySystems, verbose_name='Платежная система')
    wd_date = models.DateTimeField(verbose_name='Дата пополнения')
    wd_sum = models.FloatField(verbose_name='Сума пополнения')
    wd_status = models.IntegerField(
        verbose_name='Статус платежа',
        choices=STATUS
    )

    class Meta:
        verbose_name = 'Вывод средств'
        verbose_name_plural = 'Вывод средств'