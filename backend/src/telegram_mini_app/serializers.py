import json
from urllib.parse import unquote, parse_qs

from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class UserInitDataSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    id = serializers.IntegerField()
    language_code = serializers.CharField(required=False)
    photo_url = serializers.URLField(required=False)


class TelegramInitDataSerializer(serializers.Serializer):
    hash = serializers.CharField()
    signature = serializers.CharField(required=False)
    user = UserInitDataSerializer()


class TelegramAuthSerializer(serializers.Serializer):
    init_data = serializers.CharField()

    @staticmethod
    def parse_init_data(data):
        try:
            parsed_data = parse_qs(unquote(data.get('init_data', '')))
            for key in parsed_data:
                parsed_data[key] = parsed_data[key][0]

            parsed_data['user'] = {key: value for key, value in
                                   json.loads(parsed_data['user']).items() if value != ''}

        except (json.JSONDecodeError, ValueError, IndexError, KeyError):
            raise ValidationError("Parse init_data error")

        return parsed_data

    def validate(self, data):
        parsed_data = self.parse_init_data(data)
        serializer = TelegramInitDataSerializer(data=parsed_data)
        serializer.is_valid(raise_exception=True)
        return parsed_data
