from aiogram import Bot
from django.http import HttpResponse, HttpRequest
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
from aiogram.types import Update

from telegram_bot.utils import dp

@csrf_exempt
async def webhook(request: HttpRequest) -> HttpResponse:
    """View для обработки вебхука от Telegram."""
    if request.method == "POST":
        try:
            raw_data = request.body.decode('utf-8')

            update = Update.model_validate_json(raw_data)

            await dp.feed_update(bot=Bot(settings.TELEGRAM_BOT_TOKEN), update=update)

            return HttpResponse(status=200)

        except json.JSONDecodeError as e:
            return HttpResponse("Invalid JSON", status=400)

    return HttpResponse(status=405)