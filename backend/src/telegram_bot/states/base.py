from aiogram.fsm.state import State, StatesGroup


class TestDialog(StatesGroup):
    waiting_for_name = State()
    waiting_for_age = State()
    confirmation = State()