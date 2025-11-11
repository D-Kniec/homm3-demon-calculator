import sys
import src.db as db
import src.core
from src.config import DEMON_HP, PIT_LORD_GRIND_RATE,FACTION_COLORS

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
import questionary

console = Console()



def get_int_input(prompt: str) -> int:
    """Safely gets an integer from the user using questionary."""
    while True:
        answer = questionary.text(prompt).ask()
        try:
            return int(answer)
        except (ValueError, TypeError):
            console.print("[bold red]Error: Please enter a valid integer.[/bold red]")

def get_float_input(prompt: str) -> float:
    """Safely gets a float from the user using questionary."""
    while True:
        answer = questionary.text(prompt).ask()
        try:
            return float(answer)
        except (ValueError, TypeError):
            console.print("[bold red]Error: Please enter a valid number.[/bold red]")

def get_choice_from_map(options_map: dict):
    """Gets a user's choice from a dictionary map using questionary."""
    while True:
        choice_str = questionary.text("Enter number (or '0' to cancel/back):").ask()
        
        if choice_str is None:
            return None
        if choice_str == '0':
            return None 
        
        if choice_str in options_map:
            return options_map[choice_str]
        else:
            valid_keys = ", ".join(options_map.keys())
            console.print(f"[bold red]Error: Please select a valid number. Choices are: {valid_keys}[/bold red]")

def display_main_menu():
    """Displays the main menu using rich.Panel."""
    menu_text = (
        "\n"
        "[bold cyan][1][/bold cyan] Simple Calculator ('Sandbox' Mode)\n"
        "[bold cyan][2][/bold cyan] Game Mode (Load/Create) (TODO)\n"
        "\n"
        "[bold yellow][0][/bold yellow] Exit"
    )
    
    console.print(
        Panel(
            menu_text, 
            title="DEMON FARMING CALCULATOR (HotA)", 
            border_style="#d62455",
            title_align="center",
            padding=(1, 2)
        )
    )

def display_results(results: dict):
    """Displays a formatted calculation report using rich."""
    console.print(Panel(
        f"  [bold]INPUT DATA[/bold]\n"
        f"    ├─ Units:           {results['unit_count']} x (HP: {results['unit_hp']})\n"
        f"    ├─ Total HP Pool:   {results['total_hp_pool']:.0f}\n"
        f"    └─ Pit Lords Used:  {results['pit_lord_count']}\n"
        f"\n"
        f"  [bold]YIELD[/bold]\n"
        f"    ├─ Max (from HP):   [yellow]{results['max_demons_from_hp']:.2f}[/yellow]\n"
        f"    ├─ Max (from Lords): [yellow]{results['max_demons_from_lords']:.2f}[/yellow]\n"
        f"    └─ >> [bold green] ACTUALLY GAINED: {results['actual_demons_gained']:.2f} demons[/bold green]\n"
        f"\n"
        f"  [bold]OPTIMIZATION[/bold]\n"
        f"    ├─ Wasted HP:       [red]{results['wasted_hp']:.2f}[/red] (remainder)\n"
        f"    ├─ Needed Lords:    {results['needed_pit_lords']} (for this stack)\n"
        f"    └─ Perfect Stack:   {results['perfect_grind_units']} units (for {results['perfect_grind_hp']:.0f} HP)",
        title="Calculation Results",
        border_style="magenta",
        padding=1
    ))


def display_unit_selection_table(faction: str, non_upgraded: list, upgraded: list) -> dict:
    """Displays units in a rich.Table and returns the choice map."""
    
    faction_color = FACTION_COLORS.get(faction, "default")
    
    table = Table(title=f"Select Unit ({faction})", border_style="blue", padding=(0, 1))
    table.add_column("Key", style="cyan", width=5)
    table.add_column("Non-Upgraded")
    table.add_column("HP", style="yellow", width=6)
    table.add_column("Key", style="cyan", width=5)
    table.add_column("Upgraded")
    table.add_column("HP", style="yellow", width=6)
    
    choice_map = {}
    
    len_n = len(non_upgraded)
    len_u = len(upgraded)
    max_len = max(len_n, len_u)

    for i in range(max_len):
        key_n, unit_n_str, hp_n = "", "", ""
        if i < len_n:
            key_n = str(i + 1)
            unit_n_str = non_upgraded[i][0]
            hp_n = str(non_upgraded[i][1])
            choice_map[key_n] = non_upgraded[i]

        key_u, unit_u_str, hp_u = "", "", ""
        if i < len_u:
            key_u = str(i + 1) * 2
            unit_u_str = upgraded[i][0]
            hp_u = str(upgraded[i][1])
            choice_map[key_u] = upgraded[i]
        
        if i > 0:
            table.add_row("---", "---", "---", "---", "---", "---", style="dim")

        unit_n_styled = Text(unit_n_str, style=faction_color) if unit_n_str else ""
        unit_u_styled = Text(unit_u_str, style=faction_color) if unit_u_str else ""

        table.add_row(f"[{key_n}]", unit_n_styled, hp_n, f"[{key_u}]", unit_u_styled, hp_u)
        
    console.print(table)
    return choice_map


def display_distribution_chart(chart_data: list, user_pit_lord_input: int, next_perfect_count: int, current_count: int):
    """Draws the terminal bar chart using rich.Table."""
    
    lords_color_hex = "#FC591E"

    demons_values = [d['demons'] for d in chart_data if d.get('demons') is not None]
    if not demons_values:
        console.print("  (No data to display)")
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
        return Text('█' * bar_len, style="blue") + Text(' ' * (BAR_WIDTH - bar_len))

    table = Table.grid(padding=(0, 1))
    table.add_column(width=4)
    table.add_column(width=9)
    table.add_column(width=10)
    table.add_column(width=BAR_WIDTH + 2)
    table.add_column(width=15)
    table.add_column(width=15)
    table.add_column()

    for item in chart_data:
        if item.get('is_special'):
            table.add_row(Text("(...)".center(23 + BAR_WIDTH), style="dim"))
            current_lord_group = None 
            
        count = item['count']
        demons = item['demons']
        waste = item.get('waste')
        lords = item['lords']
        is_current = item['is_current']
        
        is_perfect = (waste is not None and waste == 0.0 and count > 0)
        
        if count == 0 and not is_current:
            continue
            
        check_mark = Text(" ")
        if lords is None:
            check_mark = Text("?", style="yellow")
        elif user_pit_lord_input >= lords:
            check_mark = Text("✓", style="green")

        lords_str = Text(" ")
        if lords != current_lord_group:
            if current_lord_group is not None:
                table.add_row(
                    Text("---", style="dim"), 
                    Text("---------", style="dim"), 
                    Text("---------", style="dim"), 
                    Text("-" * (BAR_WIDTH + 2), style="dim"), 
                    Text("---------------", style="dim"), 
                    Text("-------------------", style="dim"), 
                    style="dim"
                )

            if lords is None:
                lords_str = Text("?? lords", style="yellow")
            elif user_pit_lord_input >= lords:
                 lords_str = Text(f"{lords: >2} lord{'s' if lords != 1 else ' '}", style=f"bold {lords_color_hex}")
            else:
                 lords_str = Text(f"{lords: >2} lord{'s' if lords != 1 else ' '}", style=f"{lords_color_hex}")
            
            current_lord_group = lords
        
        label = Text("")
        if is_current and is_perfect:
            label = Text("  <-- (CURRENT & PERFECT)", style="bold green")
        elif is_current:
            label = Text("  <-- (CURRENT)", style="bold yellow")
            if next_perfect_count > current_count:
                diff = next_perfect_count - current_count
                label.append(f" (Need +{diff} for PERFECTION)", style="yellow")
        elif is_perfect:
            label = Text("  <-- (PERFECT STACK)", style="bold green")
            
        if count < 0 or demons is None:
            bar_str = Text(" (invalid) ".center(BAR_WIDTH), style="red")
            demons_str = Text("---".center(6), style="dim")
            waste_str = Text("---".center(6), style="dim")
        else:
            bar_str = get_bar(demons)
            demons_str = Text(f"{demons: >6.2f} Demons")
            waste_str = Text(f"{waste: >6.2f} HP", style="red" if waste > 0 else "dim")
            
        table.add_row(
            f"[{check_mark}]", 
            lords_str, 
            f"{count: >3} Units:",
            f"[{bar_str}]",
            demons_str,
            f"| Waste: {waste_str}",
            label
        )
    
    console.print(Panel(table, title="Local Distribution Chart", border_style="cyan"))

    legend = (
        f"    [green][✓][/green]/[dim][ ][/dim] = Your {user_pit_lord_input} Pit Lords are enough for this stack\n"
        f"    [blue]█[/blue]       = *Potential* Demons from HP (scaled to list max)\n"
        f"    [bold {lords_color_hex}]Lords[/bold {lords_color_hex}]   = *Theoretical* Pit Lords needed for this stack"
    )
    console.print(Panel(legend, title="Legend", border_style="grey50", padding=(0, 2)))


def _calculate_chart_data(unit_hp, unit_count, pit_lord_count):
    """Builds the data list for the distribution chart."""
    chart_data_list = []
    results_current = None
    
    if unit_count < 0:
        unit_count = 0
        
    results_current = src.core.calculate_demon_farm(unit_hp, unit_count, pit_lord_count)
    min_perfect_stack = results_current['perfect_grind_units']
    current_waste = results_current['wasted_hp']
    
    next_perfect_count = -1
    if min_perfect_stack > 0:
        if current_waste == 0:
            next_perfect_count = unit_count + min_perfect_stack
        else:
            next_perfect_count = ((unit_count // min_perfect_stack) + 1) * min_perfect_stack

    for offset in range(-4, 5): 
        current_count = unit_count + offset
        is_current = (offset == 0)
        
        if current_count < 0:
            continue
        
        if is_current:
            results = results_current
        else:
            results = src.core.calculate_demon_farm(unit_hp, current_count, pit_lord_count)
        
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
                results = src.core.calculate_demon_farm(unit_hp, perfect_below_count, pit_lord_count)
                chart_data_list.insert(0, {
                    'count': perfect_below_count, 
                    'demons': results['max_demons_from_hp'],
                    'waste': results['wasted_hp'], 
                    'lords': results['needed_pit_lords'], 
                    'is_current': False,
                    'is_special': True
                })

        last_item = chart_data_list[-1]
        if next_perfect_count > last_item['count']:
            results = src.core.calculate_demon_farm(unit_hp, next_perfect_count, pit_lord_count)
            chart_data_list.append({
                'count': next_perfect_count, 
                'demons': results['max_demons_from_hp'],
                'waste': results['wasted_hp'], 
                'lords': results['needed_pit_lords'], 
                'is_current': False,
                'is_special': True
            })

    return results_current, chart_data_list, next_perfect_count

def run_simple_calculator():
    """Runs the logic for the Simple Calculator."""
    
    choice = questionary.select(
        "Select unit HP source:",
        choices=[
            questionary.Choice("Select from database", '1'),
            questionary.Choice("Enter HP manually", '2'),
            questionary.Separator(),
            questionary.Choice("Back to Main Menu", '0')
        ]
    ).ask()

    unit_hp = 0.0

    if choice == '1':
        while True:
            factions = db.get_factions()
            factions.append(questionary.Separator())
            factions.append(questionary.Choice("Back", "0"))
            
            faction = questionary.select(
                "Select Faction:",
                choices=factions
            ).ask()
            
            if faction is None or faction == '0': 
                return 

            non_upgraded = db.get_units_by_faction(faction, False)
            upgraded = db.get_units_by_faction(faction, True)
            
            if not non_upgraded and not upgraded:
                console.print(f"[bold red]No units found for '{faction}'.[/bold red]")
                input("... press Enter to select another faction ...")
                continue 

            while True:
                choice_map = display_unit_selection_table(faction, non_upgraded, upgraded)
                
                unit_data = get_choice_from_map(choice_map) 
                
                if unit_data is None: 
                    break 

                unit_hp = unit_data[1] 
                
                unit_count = get_int_input(f"Enter number of units (HP: {unit_hp}): ")

                prelim_results = src.core.calculate_demon_farm(unit_hp, unit_count, 0)
                needed_lords = prelim_results['needed_pit_lords']
                
                pit_lord_count = get_int_input(f"Enter number of Pit Lords (needed: {needed_lords}): ")

                results_current, chart_data_list, next_p_count = _calculate_chart_data(unit_hp, unit_count, pit_lord_count)

                display_results(results_current)
                display_distribution_chart(chart_data_list, pit_lord_count, next_p_count, unit_count)
                
                console.print("\n... press Enter to calculate for another unit in this faction ...", style="dim")
                input()

    elif choice == '2':
        unit_hp = get_float_input("Enter single unit HP: ")
        
        unit_count = get_int_input(f"Enter number of units (HP: {unit_hp}): ")
        
        prelim_results = src.core.calculate_demon_farm(unit_hp, unit_count, 0)
        needed_lords = prelim_results['needed_pit_lords']
        
        pit_lord_count = get_int_input(f"Enter number of Pit Lords (needed: {needed_lords}): ")

        results_current, chart_data_list, next_p_count = _calculate_chart_data(unit_hp, unit_count, pit_lord_count)

        display_results(results_current)
        display_distribution_chart(chart_data_list, pit_lord_count, next_p_count, unit_count)
        
        console.print("\n... press Enter to return to the main menu ...", style="dim")
        input()
    
    elif choice == '0' or choice is None:
        return
    

def start_app():
    """Main application loop."""
    
    while True:
        display_main_menu()
        
        choice = questionary.select(
            "Select option:",
            choices=[
                questionary.Choice("Simple Calculator", '1'),
                questionary.Choice("Game Mode (TODO)", '2'),
                questionary.Separator(),
                questionary.Choice("Exit", '0')
            ],
            use_shortcuts=True
        ).ask()

        if choice == '1':
            run_simple_calculator()
        elif choice == '2':
            console.print("\n[yellow]Game Mode is not yet implemented. (TODO)[/yellow]")
            console.print("\n... press Enter to return to menu ...", style="dim")
            input()
        elif choice == '0' or choice is None:
            console.print("[bold cyan]Goodbye![/bold cyan]")
            sys.exit(0)
        else:
            console.print("[bold red]Invalid choice, please try again.[/bold red]")