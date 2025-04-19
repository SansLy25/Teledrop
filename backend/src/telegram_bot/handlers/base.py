from aiogram import Router, types, F
from aiogram.enums import ContentType

router = Router()


@router.message(
    F.content_type.in_({
        ContentType.PHOTO,
        ContentType.DOCUMENT,
        ContentType.VIDEO,
        ContentType.AUDIO,
        ContentType.VOICE
    })
)
async def file_create(message: types.Message):


    try:
        print(file.file_name)
    except Exception:
        print(file.file_id)

