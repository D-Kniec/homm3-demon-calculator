# cli.py
import sys
import db as db
import core
from config import DEMON_HP, PIT_LORD_GRIND_RATE

def get_int_input(prompt: str) -> int:
    """gets an integer input from the user."""
    while True:
        try:
            value_str = input(prompt)
            return int(value_str)
        except ValueError:
            print("Error: Please enter a valid integer.")

def get_float_input(prompt: str) -> float:
    """gets a float input from the user."""
    while True:
        try:
            value_str = input(prompt)
            return float(value_str)
        except ValueError:
            print("Error: Please enter a valid number.")

def display_options(options: list, title: str):
    """Displays a numbered list of options."""
    print(f"\n--- {title} ---")
    for i, option in enumerate(options):
        if isinstance(option, tuple):
            print(f"  [{i+1}] {option[0]} (HP: {option[1]})")
        else:
            print(f"  [{i+1}] {option}")

def get_choice(options: list):
    """Gets the user's selection from a list of options."""
    while True:
        choice_str = input("Enter number (or '0' to cancel/back): ")
        try:
            choice_int = int(choice_str)
            if choice_int == 0:
                return None 
            if 0 < choice_int <= len(options):
                return options[choice_int - 1] 
            else:
                print(f"Error: Please select a number between 1 and {len(options)}.")
        except ValueError:
            print("Error: Please enter a number.")

def display_main_menu():
    """Displays the main menu."""
    print("\n╔════════════════════════════════════════════╗")
    print("║        DEMON FARMING CALCULATOR (HotA)       ║")
    print("╠════════════════════════════════════════════╣")
    print("║ [1] Simple Calculator ('Sandbox' Mode)       ║")
    print("║ [2] Game Mode (Load/Create) (TODO)           ║")
    print("║ [0] Exit                                     ║")
    print("╚════════════════════════════════════════════╝")

def display_results(results: dict):
    """Displays a formatted calculation report."""
    print("\n--- CALCULATION RESULTS ---")
    print(f"  Unit: {results['unit_count']} x (HP: {results['unit_hp']})")
    print(f"  Total HP Pool: {results['total_hp_pool']:.0f}")
    print(f"  Pit Lords Used: {results['pit_lord_count']}")
    print("-" * 20)
    print(f"  Max demons from HP pool: {results['max_demons_from_hp']:.2f}")
    print(f"  Max demons from Pit Lords: {results['max_demons_from_lords']:.2f}")
    print(f"  ACTUALLY GAINED: {results['actual_demons_gained']:.2f} demons")
    print("-" * 20)
    print("--- Optimization ---")
    print(f"  Wasted HP (remainder): {results['wasted_hp']:.2f}") 
    print(f"  Required Pit Lords for full conversion: {results['needed_pit_lords']}")
    print(f"  Perfect stack (0 waste): {results['perfect_grind_units']} units (for {results['perfect_grind_hp']:.0f} HP)")

def display_distribution_chart(chart_data: list, user_pit_lord_input: int):
    """
    Draws a terminal bar chart, grouping results
    by the required number of Pit Lords.
    """
    print("\n--- Local Distribution Chart ---")
    
    print(" " * 12 + "  █ = *Potential* Demons from HP (scaled to list max)")
    print(" " * 12 + "  Lords = *Theoretical* Pit Lords needed for this stack")
    print(f"           [✓]/[ ] = Is your {user_pit_lord_input} Pit Lords enough for THIS GROUP?")
    
    demons_values = [d['demons'] for d in chart_data if d.get('demons') is not None]
    if not demons_values:
        print("  (No data to display)")
        return
        
    max_demons = max(demons_values)
    if max_demons == 0:
        max_demons = 1 

    BAR_WIDTH = 25 
    current_lord_group = None 

    def get_bar(demons):
        """Creates a single bar."""
        if demons is None:
            return " " * BAR_WIDTH
        bar_len = int((demons / max_demons) * BAR_WIDTH)
        return '█' * bar_len + ' ' * (BAR_WIDTH - bar_len)

    for item in chart_data:
        if item.get('is_special'):
            print(" " * 12 + "(...)")
            current_lord_group = None 
        
        count = item['count']
        demons = item['demons']
        waste = item.get('waste')
        lords = item.get('lords')
        is_current = item['is_current']
        
        is_perfect = (waste is not None and waste == 0.0 and count > 0)
        
        if count == 0 and not is_current:
            continue
            
        prefix = ""
        if lords != current_lord_group:
            if current_lord_group is not None:
                print(" " * 12 + "-" * (BAR_WIDTH + 30)) 
            
            check_mark = " "
            if lords is None:
                check_mark = "?"
            elif user_pit_lord_input >= lords:
                check_mark = "✓"
            
            if lords is None:
                prefix = f" [{check_mark}]  ?? lords"
                current_lord_group = None
            else:
                prefix = f" [{check_mark}] {lords: >2} lord{'s' if lords != 1 else ' '}"
                current_lord_group = lords
        else:
            prefix = " " * 13
            
        label = ""
        if is_current and is_perfect:
            label = " <-- CURRENT & PERFECT"
        elif is_current:
            label = " <-- CURRENT"
        elif is_perfect:
            label = " <-- PERFECT STACK"
            
        if count < 0 or demons is None:
            bar_str = " (invalid) ".center(BAR_WIDTH)
            demons_str = "---".center(6)
            waste_str = "---".center(6)
        else:
            bar_str = get_bar(demons)
            demons_str = f"{demons: >6.2f}"
            waste_str = f"{waste: >6.2f}"
            
        print(f"{prefix} | {count: >3} Units: [{bar_str}] {demons_str} Demons | Waste: {waste_str} HP{label}")

def _calculate_chart_data(unit_hp, unit_count, pit_lord_count):
    """
    Helper function to build the full chart data list.
    Creates 9 bars (-4 to +4) AND adds special '(...)' bars.
    """
    chart_data_list = []
    results_current = None
    
    if unit_count < 0:
        unit_count = 0
        
    results_current = core.calculate_demon_farm(unit_hp, unit_count, pit_lord_count)
    min_perfect_stack = results_current['perfect_grind_units']

    for offset in range(-4, 5): 
        current_count = unit_count + offset
        is_current = (offset == 0)
        
        if current_count < 0:
            continue
        
        if is_current:
            results = results_current
        else:
            results = core.calculate_demon_farm(unit_hp, current_count, pit_lord_count)
        
        demons_for_bar = results['max_demons_from_hp'] 
        wasted = results['wasted_hp']
        needed_lords = results['needed_pit_lords']
        
        chart_data_list.append({
            'count': current_count, 'demons': demons_for_bar, 
            'waste': wasted, 'lords': needed_lords, 
            'is_current': is_current
        })

    if min_perfect_stack > 0:
        first_item = chart_data_list[0]
        if first_item['count'] > 0 and (first_item['waste'] > 0 or first_item['count'] > min_perfect_stack):
            perfect_below_count = ((first_item['count'] - 1) // min_perfect_stack) * min_perfect_stack
            
            if perfect_below_count >= 0 and perfect_below_count < first_item['count']:
                results = core.calculate_demon_farm(unit_hp, perfect_below_count, pit_lord_count)
                chart_data_list.insert(0, {
                    'count': perfect_below_count, 
                    'demons': results['max_demons_from_hp'],
                    'waste': results['wasted_hp'], 
                    'lords': results['needed_pit_lords'], 
                    'is_current': False,
                    'is_special': True
                })

        last_item = chart_data_list[-1]
        if last_item['waste'] > 0:
            perfect_above_count = ((last_item['count'] // min_perfect_stack) + 1) * min_perfect_stack
            
            if perfect_above_count > last_item['count']:
                results = core.calculate_demon_farm(unit_hp, perfect_above_count, pit_lord_count)
                chart_data_list.append({
                    'count': perfect_above_count, 
                    'demons': results['max_demons_from_hp'],
                    'waste': results['wasted_hp'], 
                    'lords': results['needed_pit_lords'], 
                    'is_current': False,
                    'is_special': True
                })

    return results_current, chart_data_list


def run_simple_calculator():
    """Logic for option [1] Simple Calculator with nested loops and tree display."""
    print("\n--- Simple Calculator ---")
    print("Select unit HP source:")
    print("  [1] Select from database")
    print("  [2] Enter HP manually")
    print("  [0] Back to Main Menu")
    choice = input("Choice: ").strip()

    unit_hp = 0.0

    if choice == '1':
        while True:
            factions = db.get_factions()
            display_options(factions, "Select Faction")
            faction = get_choice(factions)
            
            if faction is None: 
                return 

            non_upgraded = db.get_units_by_faction(faction, False)
            upgraded = db.get_units_by_faction(faction, True)
            
            if not non_upgraded and not upgraded:
                print(f"No units found for '{faction}'.")
                input("... press Enter to select another faction ...")
                continue 

            all_units = non_upgraded + upgraded

            while True:
                print(f"\n--- Select Unit ({faction}) ---")
                offset = 0
                
                if non_upgraded:
                    print("  -Non-Upgraded")
                    for i, unit in enumerate(non_upgraded):
                        print(f"    ├─ [{i+1}] {unit[0]} (HP: {unit[1]})")
                    offset = len(non_upgraded)
                
                if upgraded:
                    print("  -Upgraded")
                    for i, unit in enumerate(upgraded):
                        print(f"    ├─ [{i+1+offset}] {unit[0]} (HP: {unit[1]})")
                
                print("-" * 20)
                
                unit_data = get_choice(all_units) 
                
                if unit_data is None: 
                    break 

                unit_hp = unit_data[1] 
                
                unit_count = get_int_input(f"Enter number of units (HP: {unit_hp}): ")
                pit_lord_count = get_int_input("Enter number of Pit Lords: ")

                results_current, chart_data_list = _calculate_chart_data(unit_hp, unit_count, pit_lord_count)

                display_results(results_current)
                display_distribution_chart(chart_data_list, pit_lord_count)
                
                input("\n... press Enter to calculate for another unit in this faction ...")

    elif choice == '2':
        unit_hp = get_float_input("Enter single unit HP: ")
        
        unit_count = get_int_input(f"Enter number of units (HP: {unit_hp}): ")
        pit_lord_count = get_int_input("Enter number of Pit Lords: ")

        results_current, chart_data_list = _calculate_chart_data(unit_hp, unit_count, pit_lord_count)

        display_results(results_current)
        display_distribution_chart(chart_data_list, pit_lord_count)
        
        input("\n... press Enter to return to the main menu ...")
    
    elif choice == '0':
        return
    
    else:
        print("Invalid choice.")
        input("\n... press Enter to return to the main menu ...")


def start_app():
    """Main application loop."""
    
    while True:
        display_main_menu()
        choice = input("Select option: ").strip()

        if choice == '1':
            run_simple_calculator()
        elif choice == '2':
            print("\nGame Mode is not yet implemented. (TODO)")
            input("\n... press Enter to return to menu ...")
        elif choice == '0':
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice, please try again.")