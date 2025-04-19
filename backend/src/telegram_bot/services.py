from aiogram import types
from aiogram.enums import ContentType

class FileCRUDService:
    pass


class UtilsService:
    @staticmethod
    async def get_message_files_id(message: types.Message):
        match message.content_type:
            case ContentType.PHOTO:
                file = message.photo[-1]
            case ContentType.DOCUMENT:
                file = message.document
            case ContentType.VIDEO:
                file = message.video
            case ContentType.AUDIO:
                file = message.audio
            case ContentType.VOICE:
                file = message.voice
            case _:
                return await message.answer("Неподдерживаемый тип файла")