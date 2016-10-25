from django.conf.urls import url

from .views import CommandView

urlpatterns = [
    url(r'^bot/(?P<bot_token>.+)/$', CommandView.as_view()),
]
