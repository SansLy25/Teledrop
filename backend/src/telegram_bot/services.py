import json
from aiogram import types
from aiogram.enums import ContentType

class FileCRUDService:
    pass


class FileUtilsService:
    @staticmethod
    async def get_message_file(message: types.Message):
        content_attrs_names = ["photo", "document", "video", "audio", "voice"]
        files = []
        for attr_name in content_attrs_names:
            attr_value = getattr(message, attr_name)
            if attr_value is not None:
                if isinstance(attr_value, list):
                    files.append(attr_value[-1])
                else:
                    files.append(attr_value)

        return files

    @staticmethod
    async def serialize_file(file: types.downloadable.Downloadable):
        return json.dumps(
            {
                "id": file.file_id,
                "size": file.file_size,
                "name": file.
            }
        )


