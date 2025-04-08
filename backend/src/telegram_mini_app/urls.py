from django.urls import path

from telegram_mini_app import views

urlpatterns = [path("auth/verify", views.PrimaryTelegramAuthView.as_view())]
