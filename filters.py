import re

def extract_number(text: str) -> int | None:
    match = re.findall(r'\d+', text)
    return int(match[0]) if match else None

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