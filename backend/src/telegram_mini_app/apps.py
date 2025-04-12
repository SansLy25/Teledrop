from django.apps import AppConfig


class TelegramConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "telegram_mini_app"

    def ready(self):
        import telegram_mini_app.schema
