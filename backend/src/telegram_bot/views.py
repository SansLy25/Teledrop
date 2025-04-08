import json

from celery.bin.control import status
from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.apps import apps
from aiogram.types import Update
from aiogram import Bot

from django.conf import settings

@csrf_exempt
async def webhook(request):
    if request.method == "POST":
        try:
            header_token = request.headers.get('X-Telegram-Bot-Api-Secret-Token', None)
            if header_token != settings.SECRET_KEY:
                return HttpResponse(status=403)

            dp = apps.get_app_config('telegram_bot').dp

            raw_data = request.body.decode('utf-8')
            update = Update.model_validate_json(raw_data)

            await dp.feed_update(bot=Bot(settings.TELEGRAM_BOT_TOKEN), update=update)

            return HttpResponse(status=200)

        except json.JSONDecodeError:
            return HttpResponse("Invalid JSON", status=400)

    return HttpResponse(status=405)