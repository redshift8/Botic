from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from states import Form
from keyboards import get_gender_kb, get_activity_kb, get_goal_kb
from sqlite_repo import SQLiteProfileRepo
from filters import extract_number, is_valid_target_weight
from custom_filters import ValidAgeFilter, ValidWeightFilter, ValidHeightFilter, ValidTargetWeightFilter
from abstract_repo import AbstractProfileRepo



router = Router()


@router.message(F.text == "/start")
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Я помогу вам сохранить ваши параметры\n(iба четко)")
    await message.answer("Какой у тебя пол? (не ламинат)\n\nВыбери подходящий вариант:", reply_markup=await get_gender_kb(state))
    await state.set_state(Form.gender)

@router.message(Form.gender)
async def gender_text_fallback(message: types.Message, state: FSMContext):
    await message.answer("Пожалуйста, выбери вариант из кнопок бро ", reply_markup=await get_gender_kb(state))

@router.callback_query(Form.gender, F.data.in_({"gender_male", "gender_female"}))
async def gender_selected(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(gender=callback.data)
    await callback.message.answer("Сколько тебе лет?\n\nмолоденькая?)")
    await state.set_state(Form.age)
    await callback.answer()

@router.message(Form.age, ValidAgeFilter())
async def get_age(message: types.Message, state: FSMContext, age: int):
    await state.update_data(age=age)
    await message.answer("Какой у тебя вес?\n\nВведи число:")
    await state.set_state(Form.weight)

@router.message(Form.weight, ValidWeightFilter())
async def get_weight(message: types.Message, state: FSMContext, weight: int):
    await state.update_data(weight=weight)
    await message.answer("Какой у тебя рост?\n\nВведи число в см:")
    await state.set_state(Form.height)

@router.message(Form.height, ValidHeightFilter())
async def get_height(message: types.Message, state: FSMContext, height: int):
    await state.update_data(height=height)
    await message.answer("Какой у тебя уровень активности?\n\nВыбери подходящий вариант:", reply_markup=await get_activity_kb(state))
    await state.set_state(Form.activity)

@router.message(Form.activity)
async def activity_text_fallback(message: types.Message, state: FSMContext):
    await message.answer("Выбери уровень активности через кнопки братан ", reply_markup=await get_activity_kb(state))

@router.callback_query(Form.activity, F.data.in_({
    "activity_min", "activity_low", "activity_medium", "activity_above_medium", "activity_high"}))
async def activity_selected(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(activity=callback.data)
    await callback.message.answer("Какая у тебя цель?\n\nВыбери подходящий вариант:", reply_markup=await get_goal_kb(state))
    await state.set_state(Form.goal)
    await callback.answer()

@router.callback_query(Form.goal, F.data.in_({"goal_loss", "goal_gain", "goal_maintain"}))
async def goal_selected(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(goal=callback.data)
    goal = callback.data

    if goal in {"goal_loss", "goal_gain"}:
        await callback.message.answer("Какой у тебя желаемый вес?")
        await state.set_state(Form.target_weight)
    else:
        await show_summary(callback.message, state)
        await state.clear()
    await callback.answer()

@router.message(Form.target_weight)
async def get_target_weight(message: types.Message, state: FSMContext):
    data = await state.get_data()
    goal = data.get("goal")
    current_weight = data.get("weight")

    filter = ValidTargetWeightFilter(goal, current_weight)
    result = await filter(message)
    if not result:
        return

    target_weight = result["target_weight"]
    await state.update_data(target_weight=target_weight)
    await show_summary(message, state)
    await state.clear()

GENDER_MAP = {
    "gender_male": "Мужской",
    "gender_female": "Женский"
}

ACTIVITY_MAP = {
    "activity_min": "Минимальный",
    "activity_low": "Низкий",
    "activity_medium": "Средний",
    "activity_above_medium": "Выше среднего",
    "activity_high": "Высокий"
}

GOAL_MAP = {
    "goal_loss": "Похудение",
    "goal_gain": "Набор массы",
    "goal_maintain": "Поддержание"
}


async def show_summary(message: types.Message, state: FSMContext):
    data = await state.get_data()

    gender = GENDER_MAP.get(data.get("gender"), "-")
    activity = ACTIVITY_MAP.get(data.get("activity"), "-")
    goal = GOAL_MAP.get(data.get("goal"), "-")

    text = (
        f"Твои параметры:\n"
        f"Пол: {gender}\n"
        f"Возраст: {data.get('age', '-')}\n"
        f"Вес: {data.get('weight', '-') } кг\n"
        f"Рост: {data.get('height', '-') } см\n"
        f"Активность: {activity}\n"
        f"Цель: {goal}"
    )

    if data.get("goal") in {"goal_loss", "goal_gain"}:
        text += f"\nЖелаемый вес: {data.get('target_weight')} кг"

    await message.answer(text)

    repo: AbstractProfileRepo = SQLiteProfileRepo()
    chat_id = message.chat.id
    new_id = await repo.save_profile(chat_id, data)
