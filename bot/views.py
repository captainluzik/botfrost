import json

import telebot
from django.http import HttpResponse, HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .bottest import config
from .bottest import main


class CommandView(View):
    def post(self, request, bot_token):
        # Инициализация бота.

        # Это на когда будет вебхук установлен нужно будет.
        if bot_token != config.token:
            return HttpResponseForbidden('Invalid token')
        bot = telebot.TeleBot(config.token)

        # Эта обработка неизвестной ошибки, иногда бывает так, что кто-то присылает что-то и все падает,
        # потом вебхук забивается
        # try:
        # Получение данных.
        data = self._get_data(request)
        text = self._get_command(data) or self._get_command_from_callback(data)

        # Если не None
        if text:
            # Пытаемся получить метод из модуля main, иначе None
            main_func = main.main_dict.get(text, None)
            # Если функция есть - вызываем ее с параметрами: бот и сообщение
            if main_func:
                main_func(bot, data)
        # Если прислали что-то не то - просто пропускаем это сообщение и говорим телеграму, что все норм
        # except:
        #     pass
        # Говорим телеграмму, что все хорошо
        return HttpResponse(json.dumps({'status': 200}))

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CommandView, self).dispatch(request, *args, **kwargs)

    @staticmethod
    def _get_data(request):
        # Отдаем Json.
        return json.loads(request.body.decode('utf-8'))

    @staticmethod
    def _get_command(data):
        try:
            # Парсим текст из сообщения.
            text = data['text'].lower()
        except KeyError:
            text = None
        else:
            return text

    @staticmethod
    def _get_command_from_callback(data):
        try:
            text = data['data'].lower()
        except KeyError:
            text = None
        else:
            return text
