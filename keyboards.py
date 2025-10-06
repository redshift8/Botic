from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext

async def get_gender_kb(state: FSMContext) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text="Мужской", callback_data="gender_male"),
        InlineKeyboardButton(text="Женский", callback_data="gender_female"),
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons])


async def get_activity_kb(state: FSMContext) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text="Минимальный", callback_data="activity_min"),
        InlineKeyboardButton(text="Низкий", callback_data="activity_low"),
        InlineKeyboardButton(text="Средний", callback_data="activity_medium"),
        InlineKeyboardButton(text="Выше среднего", callback_data="activity_above_medium"),
        InlineKeyboardButton(text="Высокий", callback_data="activity_high"),
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons])


async def get_goal_kb(state: FSMContext) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text="Похудение", callback_data="goal_loss"),
        InlineKeyboardButton(text="Набор массы", callback_data="goal_gain"),
        InlineKeyboardButton(text="Поддержание", callback_data="goal_maintain"),
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons])



