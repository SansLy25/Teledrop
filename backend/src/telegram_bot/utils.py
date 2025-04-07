from django.apps import apps

app_config = apps.get_app_config('telegram_bot')
bot = app_config.bot
dp = app_config.dp