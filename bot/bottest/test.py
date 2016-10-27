# coding:utf-8
import config
import telebot
from telebot import types


bot = telebot.TeleBot(config.token)
updates = bot.get_updates(1234, 100, 20)


# Везде где есть атрибут callback_data - нужно понять, какие данные будем вытягивать из базы. И так далее. Но это при написании вьюхи уже
# После старта возможность выбора языка, пока это реализовано заменой клавиатуры, но после это будет как обращение к БД
@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    markup.row('Русский', 'English')
    bot.reply_to(message, "Привет," + message.from_user.first_name + "! Выберите свой язык:", reply_markup=markup)


# Выбор языков
@bot.message_handler(regexp="Русский")
def russian(message):
    markup = types.ReplyKeyboardHide(selective=False)
    bot.send_message(message.chat.id, "Вы выбрали русский язык!", reply_markup=markup)
    keyboard = types.InlineKeyboardMarkup()
    start_button = types.InlineKeyboardButton(text="Инструкция", callback_data="test")
    keyboard.add(start_button)
    bot.send_message(message.chat.id, "Здесь напишем приветственный текст", reply_markup=keyboard)


@bot.message_handler(regexp="English")
def english(message):
    markup = types.ReplyKeyboardHide(selective=False)
    bot.send_message(message.chat.id, "Your choise is English!", reply_markup=markup)
    keyboard = types.InlineKeyboardMarkup()
    start_button = types.InlineKeyboardButton(text="FAQ", callback_data="test")
    keyboard.add(start_button)
    bot.send_message(message.chat.id, "Some English text", reply_markup=keyboard)


# Конец

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    if call.message:
        if call.data == "test":
            markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
            markup.row('Мой банк', 'Моя_команда'),
            markup.row('Чат проекта', 'Источники_дохода')
            markup.row('Настройки', 'Помощь')
            bot.send_message(call.message.chat.id, "Какая инструкция...бла бла бла", reply_markup=markup)
    # Если сообщение из инлайн-режима
    elif call.inline_message_id:
        if call.data == "test":
            bot.message_from_user(inline_message_id=call.inline_message_id, text="Инструкция")


# Блок меню "Мой банк"
@bot.message_handler(regexp="Мой банк")
def bank(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, selective=True)
    markup.row('Пополнить', 'Вывести')
    markup.row('Что-то', 'Мои взносы')
    markup.row('Что-то', 'История операций')
    markup.row('Меню')
    bot.send_message(message.chat.id, "Информация о взносах из базы", reply_markup=markup)


# "Дерево" пополнения
@bot.message_handler(regexp="Пополнить")
def enter(message):
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    btn1 = types.InlineKeyboardButton(text="10$", callback_data="1")
    btn2 = types.InlineKeyboardButton(text="20$", callback_data="2")
    btn3 = types.InlineKeyboardButton(text="50$", callback_data="3")
    btn4 = types.InlineKeyboardButton(text="Ввести в ручную", callback_data="4")
    keyboard.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, "Выберите сумму пополнения", reply_markup=keyboard)


# Конец "Дерева"
@bot.message_handler(regexp="Вывести")
def withdrawal(message):
    # тут надо будет прописать if else с положительный и\или нулевым балансом, пока заглушка
    bot.send_message(message.chat.id, "Для вывода требуется иметь хотя бы один действующий взнос в системе.")


@bot.message_handler(regexp="Мои взносы")
def balance(message):
    # та же самая фигня, как и с "Вывести". Все из базы.
    bot.send_message(message.chat.id, "У вас пока нет ни одного взноса")


@bot.message_handler(regexp="История операций")
def history(message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text="Пополнение счета", callback_data="in")
    btn2 = types.InlineKeyboardButton(text="Вывод средств", callback_data="out")
    btn3 = types.InlineKeyboardButton(text="Бонусы лояльности", callback_data="bonuses")
    btn4 = types.InlineKeyboardButton(text="Начисление процентов", callback_data="percent")
    btn5 = types.InlineKeyboardButton(text="Внутренние переводы", callback_data="inner")
    keyboard.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(message.chat.id, "Выберите тип операции ниже:", reply_markup=keyboard)


@bot.message_handler(regexp="Меню")
def down(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, selective=True)
    markup.row('Мой банк', 'Моя команда'),
    markup.row('Чат проекта', 'Источники дохода')
    markup.row('Настройки', 'Помощь')
    bot.send_message(message.chat.id, "Открываю меню...", reply_markup=markup)


# Конец "Мой банк"

# Настройки 
@bot.message_handler(regexp="Настройки")
def settings(message):
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
@bot.message_handler(regexp="Источники дохода")
def profit(message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text="Список источников, указать", callback_data="bla")
    keyboard.add(btn1)
    bot.send_message(message.chat.id, "Бла, бла, бла, про разные источники дохода", reply_markup=keyboard)


# Конец "Источники дохода"

# Помощь
@bot.message_handler(regexp="Помощь")
def help(message):
    bot.send_message(message.chat.id, "Думаю, тут и так понятно = много букафф)")


# Конец "Помощь"

# Моя команда
@bot.message_handler(regexp="Моя команда")
def myteam(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, selective=True)
    btn1 = types.KeyboardButton('Партнерская ссылка')
    btn2 = types.KeyboardButton('Промо-отдел')
    btn3 = types.KeyboardButton('Внутренний перевод')
    btn4 = types.KeyboardButton('Меню')
    markup.row(btn1, btn2)
    markup.row(btn3)
    markup.row(btn4)
    bot.send_message(message.chat.id, "Инфа про команду из базы, продумать реф.систему", reply_markup=markup)


# Конец "Моя команда"







if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)