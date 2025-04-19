from aiogram.fsm.state import StatesGroup, State


class FileUploadStatesGroup(StatesGroup):
    waiting_all_files = State()
    renaming_files = State()
