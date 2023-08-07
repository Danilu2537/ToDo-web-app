from django.urls import path

from bot.views import TgUserVerifyView

app_name = 'bot'

urlpatterns = [path('verify', TgUserVerifyView.as_view(), name='verify')]
