from aiogram.dispatcher.filters.state import StatesGroup, State

class is_city_name_given(StatesGroup):
    programm_started = State()
    getting_city_name = State()
    city_name_given = State()