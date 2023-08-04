from django.urls import include, path

from bot.views import TgUserVerifyView

app_name = 'bot'

urlpatterns = [path('verify', TgUserVerifyView.as_view(), name='verify')]
