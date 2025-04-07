from django.urls import path

from telegram_bot import views

urlpatterns = [
    path('webhook', views.webhook)
]