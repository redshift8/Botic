import re

def extract_number(text: str) -> int | None:
    match = re.findall(r'\d+', text)
    return int(match[0]) if match else None
LIMITS = {
    "age": (1, 100),
    "weight": (20, 300),
    "height": (30, 300)
}

def is_valid_feature(name: str, text: str) -> bool:
    value = extract_number(text)
    if value is None:
        return False
    min_val, max_val = LIMITS.get(name, (0, float("inf")))
    return min_val <= value <= max_val

def get_filtered_features(data: dict) -> dict:
    return {k: data[k] for k in LIMITS if k in data}

def is_valid_target_weight(goal: str, current_weight: int, text: str) -> bool:
    target = extract_number(text)
    if target is None:
        return False

    if goal == "goal_loss":
        return target < current_weight
    elif goal == "goal_gain":
        return target > current_weight
    elif goal == "goal_maintain":
        return True
    return False