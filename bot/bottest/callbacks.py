from telebot import types


class CallBack:
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
        return getattr(self, method, None)

    def russian(self):
        markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        markup.row('Банк', 'Моя команда'),
        markup.row('Чат', 'Источники_дохода')
        markup.row('Настройки', 'Помощь')
        self.bot.send_message(
            self.callback['message']['chat']['id'],
            "Какая инструкция...бла бла бла",
            reply_markup=markup
        )
        return True

    def put_10(self):
        money = self.get_money()
        if money:
            return self.bulling(money)
        return False

    def get_money(self):
        import re
        money = re.search('[0-9]+', self.callback['data'])
        if money:
            money = money.group(0)
        return money

    def bulling(self, money):
        # Будем проводить оплату
        return True