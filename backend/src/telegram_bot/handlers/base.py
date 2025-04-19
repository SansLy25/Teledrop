from typing import List

from aiogram import Router, types, F
from aiogram.enums import ContentType
import logging

from aiogram.fsm.context import FSMContext

from telegram_bot.services import FileUtilsService

router = Router()
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

@router.message(
    F.content_type.in_({
        ContentType.PHOTO,
        ContentType.DOCUMENT,
        ContentType.VIDEO,
        ContentType.AUDIO,
        ContentType.VOICE
    })
)
async def single_file_create_handler(message: types.Message, state: FSMContext):
    file = await FileUtilsService.get_message_file(message)
    await state.clear()


@router.message(
    F.content_type.in_({
        ContentType.PHOTO,
        ContentType.DOCUMENT,
        ContentType.VIDEO,
        ContentType.AUDIO,
        ContentType.VOICE
    },
    F.media_group_id)
)
async def bulk_file_create_handler(messages: List[types.Message], state: FSMContext):
    next_state = False

    if media_group_id:
        pass

    if next_state:
        await state.clear()
        await



@router.message()
async def rename_handler(message: types.Message, state: FSMContext):
    await message.answer(f"this message is file(s) {"тут все строковые представления полученных файлов"}")