import sys
import src.db as db
import src.core
import questionary
from typing import Tuple

from rich.console import Console
from rich.panel import Panel

import src.inputs as inputs
import src.views as views


console = Console()

def _get_modified_hp(base_hp: float, game_id: int, fa_level: int) -> Tuple[float, int]:
    """
    Gets the artifact bonus and calculates the modified HP.
    Returns (modified_hp, artifact_bonus)
    """
    artifact_bonus = db.get_game_hp_bonus(game_id)
    
    hp_with_artifacts = base_hp + artifact_bonus
    
    fa_multiplier = 1.0 + (fa_level * 0.10)
    
    modified_hp = hp_with_artifacts * fa_multiplier
    
    return modified_hp, artifact_bonus


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

    if choice == '1':
        last_faction = None
        while True:
            all_factions = db.get_factions()
            faction_choices = []
            if last_faction and last_faction in all_factions:
                faction_choices.append(questionary.Choice(title=f"Last Used: {last_faction}", value=last_faction))
                faction_choices.append(questionary.Separator("--- All Factions ---"))
                all_factions.remove(last_faction)
                
            for f in all_factions:
                faction_choices.append(f)
            faction_choices.append(questionary.Separator())
            faction_choices.append(questionary.Choice("Back", "0"))

            faction = questionary.select(
                "Select Faction:",
                choices=faction_choices
            ).ask()
            
            if faction is None or faction == '0': 
                return 

            last_faction = faction
            non_upgraded = db.get_units_by_faction(faction, False)
            upgraded = db.get_units_by_faction(faction, True)
            
            if not non_upgraded and not upgraded:
                console.print(f"[bold red]No units found for '{faction}'.[/bold red]")
                input("... press Enter to select another faction ...")
                continue 

            while True:
                choice_map = views.display_unit_selection_table(faction, non_upgraded, upgraded)
                unit_data = inputs.get_choice_from_map(choice_map) 
                
                if unit_data is None: 
                    break 

                unit_name, unit_hp, unit_gold_cost = unit_data
                
                unit_count = inputs.get_int_input(f"Enter number of units (HP: {unit_hp}): ")

                prelim_results = src.core.calculate_demon_farm(unit_hp, unit_count, 0)
                needed_lords = prelim_results['needed_pit_lords']
                
                pit_lord_count = inputs.get_int_input(f"Enter number of Pit Lords (needed: {needed_lords}): ", default=str(needed_lords))

                results_current, chart_data_list, next_p_count = _calculate_chart_data(unit_hp, unit_count, pit_lord_count)
                
                results_current["gold_cost"] = unit_gold_cost
                results_current["game_mode_data"] = { "unit_name": unit_name }

                views.display_results(results_current)
                views.display_distribution_chart(chart_data_list, pit_lord_count, next_p_count, unit_count)
                
                console.print("\n... press Enter to calculate for another unit in this faction ...", style="dim")
                input()

    elif choice == '2':
        unit_hp = inputs.get_float_input("Enter single unit HP: ")
        unit_count = inputs.get_int_input(f"Enter number of units (HP: {unit_hp}): ")
        
        prelim_results = src.core.calculate_demon_farm(unit_hp, unit_count, 0)
        needed_lords = prelim_results['needed_pit_lords']
        
        pit_lord_count = inputs.get_int_input(f"Enter number of Pit Lords (needed: {needed_lords}): ", default=str(needed_lords))

        results_current, chart_data_list, next_p_count = _calculate_chart_data(unit_hp, unit_count, pit_lord_count)
        
        results_current["gold_cost"] = 0

        views.display_results(results_current)
        views.display_distribution_chart(chart_data_list, pit_lord_count, next_p_count, unit_count)
        
        console.print("\n... press Enter to return to the main menu ...", style="dim")
        input()
    
    elif choice == '0' or choice is None:
        return

def run_reverse_calculator():
    """Runs the logic for the Reverse Calculator."""
    console.print(Panel("[bold]Reverse Calculator[/bold]\n\nCalculate how many units you need to get a target number of demons.", border_style="cyan"))
    
    target_demons = inputs.get_int_input("Enter target number of demons: ")
    if target_demons <= 0:
        console.print("[red]Please enter a positive number.[/red]")
        return
        
    console.print("[dim]Next, select the unit you want to sacrifice...[/dim]")
    
    last_faction = None
    while True:
        all_factions = db.get_factions()
        faction_choices = []
        if last_faction and last_faction in all_factions:
            faction_choices.append(questionary.Choice(title=f"Last Used: {last_faction}", value=last_faction))
            faction_choices.append(questionary.Separator("--- All Factions ---"))
            all_factions.remove(last_faction)
            
        for f in all_factions:
            faction_choices.append(f)
        faction_choices.append(questionary.Separator())
        faction_choices.append(questionary.Choice("Back", "0"))

        faction = questionary.select(
            "Select Faction:",
            choices=faction_choices
        ).ask()
        
        if faction is None or faction == '0': 
            return 

        last_faction = faction
        non_upgraded = db.get_units_by_faction(faction, False)
        upgraded = db.get_units_by_faction(faction, True)
        
        if not non_upgraded and not upgraded:
            console.print(f"[bold red]No units found for '{faction}'.[/bold red]")
            input("... press Enter to select another faction ...")
            continue 

        while True:
            choice_map = views.display_unit_selection_table(faction, non_upgraded, upgraded)
            unit_data = inputs.get_choice_from_map(choice_map) 
            
            if unit_data is None: 
                break 

            unit_name, unit_hp, unit_gold_cost = unit_data
            
            if unit_hp <= 0:
                console.print(f"[red]Error: {unit_name} has 0 HP and cannot be sacrificed.[/red]")
                continue

            results = src.core.calculate_reverse_farm(target_demons, unit_hp, unit_gold_cost)
            
            views.display_reverse_results(results, unit_name)
            
            console.print("\n... press Enter to calculate for another unit ...", style="dim")
            input()


def _manage_artifacts(game_id: int):
    """Handles the multi-choice selection for game artifacts."""
    
    all_artifacts = db.get_all_artifacts()
    current_artifact_ids = db.get_game_artifacts(game_id)
    
    choices = []
    for art in all_artifacts:
        choices.append(questionary.Choice(
            f"{art['name']} (+{art['hp_bonus']} HP)",
            value=art['artifact_id'],
            checked=(art['artifact_id'] in current_artifact_ids)
        ))
    
    console.print(Panel("[dim]Select the artifacts your hero possesses (space = toggle, enter = confirm)[/dim]",
                      border_style="yellow"))
    
    selected_ids = questionary.checkbox(
        "Select artifacts:",
        choices=choices
    ).ask()
    
    if selected_ids is None:
        console.print("[yellow]Artifact selection cancelled.[/yellow]")
        return

    db.set_game_artifacts(game_id, selected_ids)
    new_bonus = db.get_game_hp_bonus(game_id)
    console.print(f"\n[green]Artifacts saved! Current total HP bonus: [bold]+{new_bonus} HP[/bold][/green]")
    input("\n... press Enter to continue ...")


def _delete_game_prompt():
    """Shows a prompt to select and delete a game."""
    console.print(Panel("[bold red]Delete Game[/bold red]", border_style="red"))
    
    existing_games = db.get_all_games()
    
    if not existing_games:
        console.print("[yellow]No games found to delete.[/yellow]")
        input("\n... press Enter to continue ...")
        return

    game_choices = [
        questionary.Choice(title=f"{game['name']} (created: {game['created_at'].strftime('%Y-%m-%d')})", value=game['game_id'])
        for game in existing_games
    ]
    game_choices.append(questionary.Separator())
    game_choices.append(questionary.Choice(title="[ CANCEL ]", value=0))

    game_id_to_delete = questionary.select(
        "Which game do you want to delete? (This cannot be undone!)",
        choices=game_choices
    ).ask()

    if game_id_to_delete is None or game_id_to_delete == 0:
        console.print("[green]Deletion cancelled.[/green]")
        return

    confirm = questionary.confirm(
        f"Are you absolutely sure you want to delete this game? All logs will be lost.",
        default=False
    ).ask()

    if confirm:
        db.delete_game(game_id_to_delete)
        console.print("[green]Game successfully deleted.[/green]")
    else:
        console.print("[green]Deletion cancelled.[/green]")
        
    input("\n... press Enter to continue ...")


def run_game_mode():
    """Runs the logic for the game mode."""
    
    console.print(Panel("[bold]Game Mode[/bold]\n\nSelect a game to load or create a new one.", border_style="cyan"))
    
    existing_games = db.get_all_games()
    
    game_choices = [
        questionary.Choice(title=f"{game['name']} (created: {game['created_at'].strftime('%Y-%m-%d')})", value=game['name'])
        for game in existing_games
    ]
    
    choices = [
        questionary.Separator("--- Load Existing Game ---"),
        *game_choices,
        questionary.Separator("--- Other Options ---"),
        questionary.Choice(title="[ CREATE NEW GAME ]", value="--new--"),
        questionary.Choice(title="[ DELETE A GAME ]", value="--delete--"),
        questionary.Choice(title="[ Back to Main Menu ]", value="--back--")
    ]
    
    if not existing_games:
        choices = [
            questionary.Choice(title="[ CREATE NEW GAME ]", value="--new--"),
            questionary.Choice(title="[ DELETE A GAME ]", value="--delete--"),
            questionary.Choice(title="[ Back to Main Menu ]", value="--back--")
        ]

    selected_choice = questionary.select(
        "Select a game or create a new one:",
        choices=choices,
        use_shortcuts=True
    ).ask()
    
    game_name = ""
    
    if selected_choice is None or selected_choice == "--back--":
        return
    elif selected_choice == "--delete--":
        _delete_game_prompt()
        return
    elif selected_choice == "--new--":
        game_name = inputs.get_string_input("Enter new game name (e.g., 'my_game_02'):")
        if not game_name:
            console.print("[yellow]Game creation cancelled.[/yellow]")
            return
    else:
        game_name = selected_choice

    game_data = db.get_or_create_game(game_name)
    game_id = game_data['game_id']
    
    console.print(f"[green]Loaded game: '{game_name}'[/green]")
    
    while True:
        console.rule(f"[bold cyan]Game Mode: {game_name}[/bold cyan] | Pit Lords: {game_data['pit_lord_count']} | First Aid Lvl: {game_data['first_aid_level']}")
        
        choice = questionary.select(
            "Select action:",
            choices=[
                questionary.Choice("Farm Demons (Calculator)", '1'),
                questionary.Choice("Set Pit Lord Count", '2'),
                questionary.Choice("Set First Aid Level", '3'),
                questionary.Choice("Manage HP Artifacts", '4'),
                questionary.Choice("View Game Summary", '5S'),
                questionary.Separator(),
                questionary.Choice("Back to Main Menu", '0')
            ]
        ).ask()
        
        if choice == '0' or choice is None:
            return
        
        elif choice == '1':
            run_game_calculator_loop(game_data)
        
        elif choice == '2':
            console.print(f"Current Pit Lord count: {game_data['pit_lord_count']}")
            new_lords = inputs.get_int_input("Enter new Pit Lord count:", default=str(game_data['pit_lord_count']))
            
            db.update_game_stats(game_id, new_lords, game_data['first_aid_level'])
            game_data['pit_lord_count'] = new_lords
            
            console.print("[green]Game settings saved.[/green]")
            input("\n... press Enter to continue ...")

        elif choice == '3':
            console.print(f"Current First Aid level: {game_data['first_aid_level']} (0=None, 1=Basic, 2=Adv, 3=Exp)")
            new_fa = inputs.get_int_input("Enter new First Aid level (0-3):", default=str(game_data['first_aid_level']))
            
            if new_fa not in [0, 1, 2, 3]:
                console.print("[red]Error: First Aid level must be between 0 and 3.[/red]")
            else:
                db.update_game_stats(game_id, game_data['pit_lord_count'], new_fa)
                game_data['first_aid_level'] = new_fa
                console.print("[green]Game settings saved.[/green]")
            
            input("\n... press Enter to continue ...")

        elif choice == '4':
            _manage_artifacts(game_id)

        elif choice == '5S':
            summary_data = db.get_game_log_summary(game_id)
            views.display_game_summary(game_name, summary_data)
            input("\n... press Enter to continue ...")


def run_game_calculator_loop(game_data: dict):
    """The calculator loop used within Game Mode."""
    
    game_id = game_data['game_id']
    default_pit_lord_count = game_data['pit_lord_count']
    fa_level = game_data['first_aid_level']
    
    if default_pit_lord_count == 0:
        console.print("[bold yellow]Warning: Default Pit Lord count for this game is 0.[/bold yellow]")
        console.print("You can change this in the 'Set Pit Lord Count' menu.")

    choice = questionary.select(
        "Select unit HP source:",
        choices=[
            questionary.Choice("Select from database", 'db'),
            questionary.Choice("Enter HP manually", 'manual'),
            questionary.Separator(),
            questionary.Choice("Back to Game Menu", '0')
        ],
        default='db'
    ).ask()

    if choice == 'db':
        last_faction = None
        while True:
            all_factions = db.get_factions()
            faction_choices = []
            if last_faction and last_faction in all_factions:
                faction_choices.append(questionary.Choice(title=f"Last Used: {last_faction}", value=last_faction))
                faction_choices.append(questionary.Separator("--- All Factions ---"))
                all_factions.remove(last_faction)
                
            for f in all_factions:
                faction_choices.append(f)
            faction_choices.append(questionary.Separator())
            faction_choices.append(questionary.Choice("Back", "0"))
            
            faction = questionary.select(
                "Select Faction:",
                choices=faction_choices
            ).ask()
            
            if faction is None or faction == '0': 
                return

            last_faction = faction
            non_upgraded = db.get_units_by_faction(faction, False)
            upgraded = db.get_units_by_faction(faction, True)
            
            if not non_upgraded and not upgraded:
                console.print(f"[bold red]No units found for faction '{faction}'.[/bold red]")
                input("... press Enter to select another faction ...")
                continue 

            while True:
                choice_map = views.display_unit_selection_table(faction, non_upgraded, upgraded)
                unit_data = inputs.get_choice_from_map(choice_map) 
                
                if unit_data is None: 
                    break

                unit_name, base_hp, unit_gold_cost = unit_data
                
                modified_hp, artifact_bonus = _get_modified_hp(base_hp, game_id, fa_level)
                
                unit_count = inputs.get_int_input(f"Number of units ({unit_name} | Base HP: {base_hp} -> Mod: {modified_hp:.2f}): ")

                prelim_results_db = src.core.calculate_demon_farm(modified_hp, unit_count, 0)
                needed_lords_db = prelim_results_db['needed_pit_lords']

                current_pit_lords = inputs.get_int_input(
                    f"Enter number of Pit Lords (needed: {needed_lords_db}): ", 
                    default=str(default_pit_lord_count)
                )
                
                default_pit_lord_count = current_pit_lords 

                results_current, chart_data_list, next_p_count = _calculate_chart_data(modified_hp, unit_count, current_pit_lords)

                game_mode_info = {
                    "unit_name": unit_name,
                    "base_hp": base_hp,
                    "art_bonus": artifact_bonus,
                    "fa_level": fa_level
                }
                results_current["pit_lord_count"] = current_pit_lords
                results_current["gold_cost"] = unit_gold_cost
                results_current["game_mode_data"] = game_mode_info

                views.display_results(results_current)
                views.display_distribution_chart(chart_data_list, current_pit_lords, next_p_count, unit_count)
                
                db.log_calculation(
                    game_id=game_id,
                    unit_name=unit_name,
                    base_hp=base_hp,
                    mod_hp=modified_hp,
                    count=unit_count,
                    pit_lords=current_pit_lords,
                    demons=results_current['actual_demons_gained'],
                    waste=results_current['wasted_hp']
                )
                console.print("[bold green]✓ Result saved to game log.[/bold green]")
                
                console.print("\n... press Enter to calculate for another unit ...", style="dim")
                input()
    
    elif choice == 'manual':
        base_hp = inputs.get_float_input("Enter single unit Base HP: ")
        unit_name = f"Custom Unit ({base_hp} HP)"
        
        modified_hp, artifact_bonus = _get_modified_hp(base_hp, game_id, fa_level)
        
        unit_count = inputs.get_int_input(f"Number of units ({unit_name} | Base HP: {base_hp} -> Mod: {modified_hp:.2f}): ")

        prelim_results_manual = src.core.calculate_demon_farm(modified_hp, unit_count, 0)
        needed_lords_manual = prelim_results_manual['needed_pit_lords']

        current_pit_lords = inputs.get_int_input(
            f"Enter number of Pit Lords (needed: {needed_lords_manual}): ", 
            default=str(default_pit_lord_count)
        )
        
        default_pit_lord_count = current_pit_lords

        results_current, chart_data_list, next_p_count = _calculate_chart_data(modified_hp, unit_count, current_pit_lords)

        game_mode_info = {
            "unit_name": unit_name,
            "base_hp": base_hp,
            "art_bonus": artifact_bonus,
            "fa_level": fa_level
        }
        results_current["pit_lord_count"] = current_pit_lords
        results_current["gold_cost"] = 0
        results_current["game_mode_data"] = game_mode_info

        views.display_results(results_current)
        views.display_distribution_chart(chart_data_list, current_pit_lords, next_p_count, unit_count)
        
        db.log_calculation(
            game_id=game_id,
            unit_name=unit_name,
            base_hp=base_hp,
            mod_hp=modified_hp,
            count=unit_count,
            pit_lords=current_pit_lords,
            demons=results_current['actual_demons_gained'],
            waste=results_current['wasted_hp']
        )
        console.print("[bold green]✓ Result saved to game log.[/bold green]")
        console.print("\n... press Enter to return to game menu ...", style="dim")
        input()

    elif choice == '0' or choice is None:
        return


def start_app():
    """Main application loop."""
    
    while True:
        views.display_main_menu()
        
        choice = questionary.select(
            "Select option:",
            choices=[
                questionary.Choice("Simple Calculator", '1'),
                questionary.Choice("Game Mode (Load/Create)", '2'),
                questionary.Choice("Reverse Calculator (Demons -> Units)", '3'),
                questionary.Separator(),
                questionary.Choice("Exit", '0')
            ],
            use_shortcuts=True
        ).ask()

        if choice == '1':
            run_simple_calculator()
        elif choice == '2':
            run_game_mode()
        elif choice == '3':
            run_reverse_calculator()
        elif choice == '0' or choice is None:
            console.print("[bold cyan]Goodbye![/bold cyan]")
            sys.exit(0)
        else:
            console.print("[bold red]Invalid choice, please try again.[/bold red]")