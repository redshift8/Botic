from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    choose_action = State()
    gender = State()
    age = State()
    weight = State()
    height = State()
    activity = State()
    goal = State()
