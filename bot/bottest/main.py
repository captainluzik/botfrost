# coding:utf-8

from bot.bottest import config
import telebot
from telebot import types

from bot.bottest.callbacks import CallBack
from bot.models import Users

"""
    Везде где есть атрибут callback_data - нужно понять, какие данные будем вытягивать из базы. И так далее.
    Но это при написании вьюхи уже
    После старта возможность выбора языка, пока это реализовано заменой клавиатуры, но после это будет как обращение к БД
"""


def start(bot, message):
    markup = types.ReplyKeyboardMarkup()
    markup.row('Русский', 'English')
    user, create = Users.objects.get_or_create(
        username=message['from_user']['first_name'],
        id_user=message['from_user']['id']
    )
    bot.send_message(
        message['chat']['id'],
        "Привет, {}! Выберите свой язык:".format(user.username),
        reply_markup=markup
    )


# # Выбор языков

def russian(bot, message):
    markup = types.ReplyKeyboardHide(selective=False)
    bot.send_message(message['chat']['id'], "Вы выбрали русский язык!", reply_markup=markup)
    keyboard = types.InlineKeyboardMarkup()
    start_button = types.InlineKeyboardButton(text="Инструкция", callback_data="instruction")
    keyboard.add(start_button)
    bot.send_message(message['chat']['id'], "Здесь напишем приветственный текст", reply_markup=keyboard)


# @bot.message_handler(regexp="English")
# def english(message):
#     markup = types.ReplyKeyboardHide(selective=False)
#     bot.send_message(message.chat.id, "Your choise is English!", reply_markup=markup)
#     keyboard = types.InlineKeyboardMarkup()
#     start_button = types.InlineKeyboardButton(text="FAQ", callback_data="test")
#     keyboard.add(start_button)
#     bot.send_message(message.chat.id, "Some English text", reply_markup=keyboard)
#
#
def callback_inline(bot, call):
    # Если сообщение из чата с ботом
    if call['message']:
        CallBack(bot, call)


# # Блок меню "Мой банк"
def bank(bot, message):
    markup = types.ReplyKeyboardMarkup(row_width=2, selective=True)
    markup.row('Пополнить', 'Вывести')
    markup.row('Что-то', 'Мои взносы')
    markup.row('Что-то', 'История операций')
    markup.row('Меню')
    bot.send_message(message.chat.id, "Информация о взносах из базы", reply_markup=markup)


def choice_system(bot, message):
    markup = types.ReplyKeyboardMarkup(row_width=1, selective=True)
    markup.row('платежка_1', 'платежка_2')
    bot.send_message(message.chat.id, "Выберите платежную систему", reply_markup=markup)


# "Дерево" пополнения
def enter(bot, message):
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    # btn1 = types.InlineKeyboardButton(text="10$", callback_data="put_10")
    # btn2 = types.InlineKeyboardButton(text="20$", callback_data="put_20")
    # btn3 = types.InlineKeyboardButton(text="50$", callback_data="put_50")
    # btn4 = types.InlineKeyboardButton(text="100$", callback_data="put_100")
    # btn5 = types.InlineKeyboardButton(text="200$", callback_data="put_200")
    # btn6 = types.InlineKeyboardButton(text="500$", callback_data="put_500")
    # btn7 = types.InlineKeyboardButton(text="Ввести в ручную", callback_data="put_custom")
    # keyboard.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
    bot.send_message(message.chat.id, "Выберите сумму пополнения", reply_markup=keyboard)


# Конец "Дерева"
def withdrawal(bot, message):
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    btn1 = types.InlineKeyboardButton(text="10$", callback_data="get_10")
    btn2 = types.InlineKeyboardButton(text="20$", callback_data="get_20")
    btn3 = types.InlineKeyboardButton(text="50$", callback_data="get_50")
    btn4 = types.InlineKeyboardButton(text="100$", callback_data="get_100")
    btn5 = types.InlineKeyboardButton(text="200$", callback_data="get_200")
    btn6 = types.InlineKeyboardButton(text="500$", callback_data="get_500")
    # btn7 = types.InlineKeyboardButton(text="Ввести в ручную", callback_data="put_custom")
    keyboard.add(btn1, btn2, btn3, btn4, btn5, btn6)
    bot.send_message(message.chat.id, "Выберите сумму вывода", reply_markup=keyboard)


def balance(bot, message):
    # та же самая фигня, как и с "Вывести". Все из базы.
    bot.send_message(message.chat.id, "У вас пока нет ни одного взноса")


def history(bot, message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text="Пополнение счета", callback_data="in")
    btn2 = types.InlineKeyboardButton(text="Вывод средств", callback_data="out")
    btn3 = types.InlineKeyboardButton(text="Бонусы лояльности", callback_data="bonuses")
    btn4 = types.InlineKeyboardButton(text="Начисление процентов", callback_data="percent")
    btn5 = types.InlineKeyboardButton(text="Внутренние переводы", callback_data="inner")
    keyboard.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(message.chat.id, "Выберите тип операции ниже:", reply_markup=keyboard)


def down(bot, message):
    markup = types.ReplyKeyboardMarkup(row_width=2, selective=True)
    markup.row('Банк', 'Моя_команда'),
    markup.row('Чат', 'Источники_дохода')
    markup.row('Настройки', 'Помощь')
    bot.send_message(message.chat.id, "Открываю меню...", reply_markup=markup)


# Конец "Мой банк"

# Настройки
def settings(bot, message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(text="Сменить ник", callback_data="change_nicname")
    btn2 = types.InlineKeyboardButton(text="Стать анонимом? Надо ли?", callback_data="make_anon")
    btn3 = types.InlineKeyboardButton(text="Платежные данные", callback_data="pay_purses")
    btn4 = types.InlineKeyboardButton(text="Язык", callback_data="change_lang")
    keyboard.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id,
                     "- Текущий ник: " + message.from_user.username, reply_markup=keyboard)


# Конец "Настройки"

# Источники дохода
def profit(bot, message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text="Список источников, указать", callback_data="bla")
    keyboard.add(btn1)
    bot.send_message(message.chat.id, "Бла, бла, бла, про разные источники дохода", reply_markup=keyboard)


# Конец "Источники дохода"

# Помощь
def help(bot, message):
    bot.send_message(message.chat.id, "Думаю, тут и так понятно = много букафф)")


# Конец "Помощь"

# Моя команда
def myteam(bot, message):
    markup = types.ReplyKeyboardMarkup(row_width=2, selective=True)
    btn1 = types.KeyboardButton('Партнерская ссылка')
    btn2 = types.KeyboardButton('Промо-отдел')
    btn3 = types.KeyboardButton('Внутренний перевод')
    btn4 = types.KeyboardButton('Меню')
    markup.row(btn1, btn2)
    markup.row(btn3)
    markup.row(btn4)
    bot.send_message(message.chat.id, "Инфа про команду из базы, продумать реф.систему", reply_markup=markup)


main_dict = {
    'start': start,
    'русский': russian,
    'банк': bank,
    'пополнить': choice_system,
    'моя_команда': myteam,
    'помощь': help,
    'источники_дохода': profit,
    'настройки': settings,
    'баланс': balance,
    'платежка_1': enter,
    'вывести': withdrawal,

    'instruction': callback_inline,
    'get_10': callback_inline,
    'get_20': callback_inline,
    'get_50': callback_inline,
    'get_100': callback_inline,
    'get_200': callback_inline,
    'get_500': callback_inline,
}
