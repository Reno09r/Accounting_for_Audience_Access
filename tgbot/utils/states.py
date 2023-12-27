from aiogram.fsm.state import StatesGroup, State

class SearchState(StatesGroup):
    searching = State()

class RegistrationState(StatesGroup):
    entering_card_id = State()