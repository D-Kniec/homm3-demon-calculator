import math
from src.config import DEMON_HP, PIT_LORD_GRIND_RATE

def calculate_demon_farm(unit_hp: float, unit_count: int, pit_lord_count: int) -> dict:
    """
    Performs all calculations for demon farming based on provided inputs.
    
    Returns:
        A dictionary containing all calculated results.
    """
    
    total_hp_pool = unit_count * unit_hp
    
    max_demons_from_hp = total_hp_pool / DEMON_HP
    max_demons_from_lords = (pit_lord_count * PIT_LORD_GRIND_RATE) / DEMON_HP
    
    actual_demons_gained = min(max_demons_from_hp, max_demons_from_lords)
    
    needed_pit_lords = math.ceil(total_hp_pool / PIT_LORD_GRIND_RATE)
    wasted_hp = total_hp_pool % DEMON_HP
    
    try:
        gcd = math.gcd(int(unit_hp), DEMON_HP)
        units_for_perfect_grind = int(DEMON_HP / gcd)
        hp_for_perfect_grind = units_for_perfect_grind * unit_hp
        lords_for_perfect_grind = math.ceil(hp_for_perfect_grind / PIT_LORD_GRIND_RATE)
    except ValueError:
        units_for_perfect_grind = 0
        hp_for_perfect_grind = 0
        lords_for_perfect_grind = 0

    return {
        "unit_hp": unit_hp,
        "unit_count": unit_count,
        "pit_lord_count": pit_lord_count,
        "total_hp_pool": total_hp_pool,
        "max_demons_from_hp": max_demons_from_hp,
        "max_demons_from_lords": max_demons_from_lords,
        "actual_demons_gained": actual_demons_gained,
        "needed_pit_lords": needed_pit_lords,
        "wasted_hp": wasted_hp,
        "perfect_grind_units": units_for_perfect_grind,
        "perfect_grind_hp": hp_for_perfect_grind,
        "perfect_grind_lords": lords_for_perfect_grind,
    }

def calculate_reverse_farm(target_demons: int, unit_hp: float, unit_gold_cost: int) -> dict:
    """
    Calculates the number of units needed to produce a target number of demons.
    """
    if unit_hp <= 0:
        return { "error": "Unit HP must be positive." }

    needed_total_hp = target_demons * DEMON_HP
    
    needed_units = math.ceil(needed_total_hp / unit_hp)
    
    actual_hp_pool = needed_units * unit_hp
    actual_demons_yield = actual_hp_pool / DEMON_HP
    needed_pit_lords = math.ceil(actual_hp_pool / PIT_LORD_GRIND_RATE)
    wasted_hp = actual_hp_pool % DEMON_HP
    
    total_gold_cost = needed_units * unit_gold_cost if unit_gold_cost > 0 else 0
    gold_per_demon = total_gold_cost / actual_demons_yield if actual_demons_yield > 0 and total_gold_cost > 0 else 0
    
    return {
        "target_demons": target_demons,
        "unit_hp": unit_hp,
        "unit_gold_cost": unit_gold_cost,
        "needed_units": needed_units,
        "needed_pit_lords": needed_pit_lords,
        "actual_hp_pool": actual_hp_pool,
        "actual_demons_yield": actual_demons_yield,
        "wasted_hp": wasted_hp,
        "total_gold_cost": total_gold_cost,
        "gold_per_demon": gold_per_demon
    }