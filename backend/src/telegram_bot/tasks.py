import requests
from celery import shared_task
from django.conf import settings


@shared_task
def send_telegram_reply(message):
    name = message["message"]["from"]["first_name"]
    text = message["message"]["text"]
    chat_id = message["message"]["chat"]["id"]

    reply = f"Hi {name}! Got your message: {text}"

    reply_url = f"https://api.telegram.org/bot{settings.TELEGRAM_API_TOKEN}/sendMessage"

    data = {"chat_id": chat_id, "text": reply}

    requests.post(reply_url, data=data)