
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