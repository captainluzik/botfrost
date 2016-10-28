import datetime

from django.db import transaction
from telebot import types

from bot.libs.perfect_money import PerfectMoney
from bot.models import Withdrawal, Users, PaySystems


class CallBack:
    gets = [
        'get_10',
        'get_20',
        'get_50',
        'get_100',
        'get_200',
        'get_500',
    ]

    def __init__(self, bot, callback):
        self.bot = bot
        self.callback = callback

        self.go()

    def go(self):
        method = self.callback['data']
        method = self._get_method(method)
        if not method:
            return False
        return method()

    def _get_method(self, method):
        if method in self.gets:
            return self.get_money
        return getattr(self, method, None)

    def instruction(self):
        markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        markup.row('Банк', 'Моя_команда'),
        markup.row('Чат', 'Источники_дохода')
        markup.row('Настройки', 'Помощь')
        self.bot.send_message(
            self.callback['message']['chat']['id'],
            "Какая инструкция...бла бла бла",
            reply_markup=markup
        )
        return True

    def get_money(self):
        money = self.get_count_money()
        if money:
            return self.billing(money)
        return False

    def get_count_money(self):
        import re
        money = re.search('[0-9]+', self.callback['data'])
        if money:
            money = money.group(0)
        return money

    def billing(self, money):
        """
            {
                'PAYMENT_ID': '123',
                'Payer_Account': 'U1911111',
                'PAYMENT_AMOUNT': '0.01',
                'PAYMENT_BATCH_NUM': '1166150',
                'Payee_Account': 'U11232323'
            }
        """

        user_id = self.callback['from_user']['id']
        current_user = Users.objects.get(id_user=user_id)
        date_time = datetime.datetime.now()

        payer = 'U13776800'
        payee = 'U13289729'
        memo = None
        payment_id = None

        pm = PerfectMoney(4337475, '586945capbaby')
        res = pm.transfer(payer, payee, 0.1, memo, payment_id)
        if pm.error:
            return pm.error
        Withdrawal.objects.create(
            username=current_user,
            wd_id=int(res['PAYMENT_BATCH_NUM']),
            wd_date=date_time,
            wd_sum=float(res['PAYMENT_AMOUNT']),
            wd_status=1,
            wd_ps=PaySystems.objects.first()
        )
        return True
