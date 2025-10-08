from aiogram.filters import BaseFilter
from aiogram.types import Message
from filters import extract_number, is_valid_target_weight

LIMITS = {
    "age": (1, 100),
    "weight": (20, 300),
    "height": (30, 300)
}

class ValidAgeFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool | dict:
        value = extract_number(message.text)
        if value is None or not (LIMITS["age"][0] <= value <= LIMITS["age"][1]):
            await message.answer("Возраст должен быть от 1 до 100.")
            return False
        return {"age": value}

class ValidWeightFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool | dict:
        value = extract_number(message.text)
        if value is None or not (LIMITS["weight"][0] <= value <= LIMITS["weight"][1]):
            await message.answer("Вес должен быть от 20 до 300 кг.")
            return False
        return {"weight": value}

class ValidHeightFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool | dict:
        value = extract_number(message.text)
        if value is None or not (LIMITS["height"][0] <= value <= LIMITS["height"][1]):
            await message.answer("Рост должен быть от 30 до 300 см.")
            return False
        return {"height": value}

class ValidTargetWeightFilter(BaseFilter):
    def __init__(self, goal: str, current_weight: int):
        self.goal = goal
        self.current_weight = current_weight

    async def __call__(self, message: Message) -> bool | dict:
        value = extract_number(message.text)
        if value is None or not (LIMITS["weight"][0] <= value <= LIMITS["weight"][1]):
            await message.answer("Вес должен быть от 20 до 300 кг.")
            return False
        if not is_valid_target_weight(self.goal, self.current_weight, message.text):
            if self.goal == "goal_loss":
                await message.answer("Желаемый вес должен быть меньше текущего.")
            elif self.goal == "goal_gain":
                await message.answer("Желаемый вес должен быть больше текущего.")
            return False
        return {"target_weight": value}
