from django.urls import path

from telegram import views

urlpatterns = [
    path("auth/verify", views.PrimaryTelegramAuthView.as_view())
]