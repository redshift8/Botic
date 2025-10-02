from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
action_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Записать параметры")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

gender_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Мужской")],
        [KeyboardButton(text="Женский")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

activity_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Минимальный")],
        [KeyboardButton(text="Низкий")],
        [KeyboardButton(text="Средний")],
        [KeyboardButton(text="Выше среднего")],
        [KeyboardButton(text="Высокий")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

goal_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Похудение")],
        [KeyboardButton(text="Набор массы")],
        [KeyboardButton(text="Поддержание")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)



