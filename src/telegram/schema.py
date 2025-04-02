from drf_spectacular.extensions import OpenApiAuthenticationExtension


class TelegramInitDataAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'telegram.auth.TelegramInitDataAuth'
    name = 'telegramMiniAppsAuth'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Telegram Mini Apps InitData\n\nИспользуйте формат: `tma <init_data>`'
        }