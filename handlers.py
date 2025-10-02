import re
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from states import Form
from keyboards import gender_kb, activity_kb, goal_kb

router = Router()

@router.message(F.text == "/start")
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Я помогу вам сохранить ваши параметры\n(iба четко)",
    )
    await message.answer(
        "Какой у тебя пол? (не ламинат)\n\nВыбери подходящий вариант:",
        reply_markup=gender_kb
    )
    await state.set_state(Form.gender)

def extract_number(text):
    match = re.findall(r'\d+', text)
    return int(match[0]) if match else None

@router.message(Form.choose_action)
async def choose_action(message: types.Message, state: FSMContext):
    pass

@router.message(Form.gender)
async def get_gender(message: types.Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await message.answer(
        "Сколько тебе лет?\n\n молоденькая?)"
    )
    await state.set_state(Form.age)

@router.message(Form.age)
async def get_age(message: types.Message, state: FSMContext):
    age = extract_number(message.text)
    if not age or age > 100:
        await message.answer("Возраст должен быть числом до 100.")
        return
    await state.update_data(age=age)
    await message.answer(
        "Какой у тебя вес?\n\nВведи число:"
    )
    await state.set_state(Form.weight)

@router.message(Form.weight)
async def get_weight(message: types.Message, state: FSMContext):
    weight = extract_number(message.text)
    if not weight or weight > 300:
        await message.answer("Вес должен быть числом до 300 кг.")
        return
    await state.update_data(weight=weight)
    await message.answer(
        "Какой у тебя рост?\n\nВведи число в см:"
    )
    await state.set_state(Form.height)

@router.message(Form.height)
async def get_height(message: types.Message, state: FSMContext):
    height = extract_number(message.text)
    if not height or height > 300:
        await message.answer("Рост должен быть числом до 300 см.")
        return
    await state.update_data(height=height)
    await message.answer(
        "Какой у тебя уровень активности?\n\nВыбери подходящий вариант:",
        reply_markup=activity_kb
    )
    await state.set_state(Form.activity)

@router.message(Form.activity)
async def get_activity(message: types.Message, state: FSMContext):
    await state.update_data(activity=message.text)
    await message.answer(
        "Какая у тебя цель?\n\nВыбери подходящий вариант:",
        reply_markup=goal_kb
    )
    await state.set_state(Form.goal)

@router.message(Form.goal)
async def get_goal(message: types.Message, state: FSMContext):
    await state.update_data(goal=message.text)
    data = await state.get_data()
    text = (
        f"Твои параметры:\n"
        f"Пол: {data.get('gender', '-') }\n"
        f"Возраст: {data.get('age', '-') }\n"
        f"Вес: {data.get('weight', '-') } кг\n"
        f"Рост: {data.get('height', '-') } см\n"
        f"Активность: {data.get('activity', '-') }\n"
        f"Цель: {data.get('goal', '-') }"
    )
    await message.answer(text)
    await state.clear()


