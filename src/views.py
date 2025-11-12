from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from src.config import FACTION_COLORS, DEMON_GOLD_COST 

console = Console()

def display_main_menu():
    """Displays the main menu using rich.Panel."""
    menu_text = (
        "\n"
        "[bold cyan][1][/bold cyan] Simple Calculator ('Sandbox' Mode)\n"
        "[bold cyan][2][/bold cyan] Game Mode (Load/Create)\n"
        "[bold cyan][3][/bold cyan] Reverse Calculator (Demons -> Units)\n"
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
    """
    Displays a formatted calculation report using rich.
    Handles both simple mode and game mode (with HP modifiers).
    """
    
    game_mode_data = results.get("game_mode_data")
    unit_gold_cost = results.get("gold_cost", 0)
    
    hp_section = ""
    if game_mode_data:
        g = game_mode_data
        base = g.get('base_hp', results['unit_hp'])
        art = g.get('art_bonus', 0)
        fa_lvl = g.get('fa_level', 0)
        fa_perc = fa_lvl * 10
        mod_hp = results['unit_hp']

        if 'base_hp' in g:
            hp_section = (
                f"    ├─ Base HP:         {base:.1f}\n"
                f"    ├─ Artifact Bonus:  +{art}\n"
                f"    ├─ First Aid Lvl:   {fa_lvl} ({fa_perc}%)\n"
                f"    └─ [bold]Modified HP:     {mod_hp:.2f}[/bold]\n"
            )
        else:
            hp_section = (
                f"    ├─ Unit HP:         {results['unit_hp']}\n"
            )
    else:
        hp_section = (
            f"    ├─ Unit HP:         {results['unit_hp']}\n"
        )

    pit_lord_section = f"    └─ Pit Lords Used:  {results['pit_lord_count']}\n"
    if game_mode_data and 'base_hp' in game_mode_data:
        pit_lord_section = f"    └─ Pit Lords Used:  {results['pit_lord_count']}\n"

    unit_display_name = "Custom"
    if game_mode_data:
        unit_display_name = game_mode_data.get('unit_name', 'Custom')

    economics_section = ""
    if unit_gold_cost > 0:
        total_gold_cost = results['unit_count'] * unit_gold_cost
        actual_demons = results['actual_demons_gained']
        gold_per_demon = (total_gold_cost / actual_demons) if actual_demons > 0 else 0
        
        profit_loss_line = ""
        if gold_per_demon > 0:
            profit_loss = DEMON_GOLD_COST - gold_per_demon
            if profit_loss > 0:
                profit_loss_line = f"    └─ Profit vs Buying:  [bold green]+{profit_loss:,.0f} gold / demon[/bold green]\n"
            else:
                profit_loss_line = f"    └─ Loss vs Buying:    [bold red]{profit_loss:,.0f} gold / demon[/bold red]\n"

        economics_section = (
            f"\n"
            f"  [bold]ECONOMICS[/bold]\n"
            f"    ├─ Unit Cost:       [yellow]{unit_gold_cost:,.0f} gold[/yellow]\n"
            f"    ├─ Total Stack Cost:[yellow]{total_gold_cost:,.0f} gold[/yellow]\n"
            f"    ├─ Cost per Demon:  [bold yellow]{gold_per_demon:,.0f} gold[/bold yellow]\n"
            f"{profit_loss_line}"
        )
    
    console.print(Panel(
        f"  [bold]INPUT DATA[/bold]\n"
        f"    ├─ Units:           {results['unit_count']} x (Unit: {unit_display_name})\n"
        f"{hp_section}"
        f"    ├─ Total HP Pool:   {results['total_hp_pool']:.0f} (from Modified HP)\n"
        f"{pit_lord_section}"
        f"\n"
        f"  [bold]YIELD[/bold]\n"
        f"    ├─ Max (from HP):   [yellow]{results['max_demons_from_hp']:.2f}[/yellow]\n"
        f"    ├─ Max (from Lords): [yellow]{results['max_demons_from_lords']:.2f}[/yellow]\n"
        f"    └─ >> [bold green] ACTUALLY GAINED: {results['actual_demons_gained']:.2f} demons[/bold green]\n"
        f"\n"
        f"  [bold]OPTIMIZATION (Based on [underline]Modified HP[/underline])[/bold]\n"
        f"    ├─ Wasted HP:       [red]{results['wasted_hp']:.2f}[/red] (remainder)\n"
        f"    ├─ Needed Lords:    {results['needed_pit_lords']} (for this stack)\n"
        f"    └─ Perfect Stack:   {results['perfect_grind_units']} units (for {results['perfect_grind_hp']:.0f} HP)"
        f"{economics_section}",
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
    table.add_column("Cost", style="yellow", width=7)
    table.add_column("Key", style="cyan", width=5)
    table.add_column("Upgraded")
    table.add_column("HP", style="yellow", width=6)
    table.add_column("Cost", style="yellow", width=7)
    
    choice_map = {}
    
    len_n = len(non_upgraded)
    len_u = len(upgraded)
    max_len = max(len_n, len_u)

    for i in range(max_len):
        key_n, unit_n_str, hp_n, cost_n = "", "", "", ""
        if i < len_n:
            key_n = str(i + 1)
            unit_n_str = non_upgraded[i][0]
            hp_n_val = non_upgraded[i][1]
            cost_n_val = non_upgraded[i][2]
            hp_n = str(hp_n_val)
            cost_n = str(cost_n_val) if cost_n_val > 0 else "N/A"
            choice_map[key_n] = (unit_n_str, float(hp_n_val), int(cost_n_val))

        key_u, unit_u_str, hp_u, cost_u = "", "", "", ""
        if i < len_u:
            key_u = str(i + 1) * 2
            unit_u_str = upgraded[i][0]
            hp_u_val = upgraded[i][1]
            cost_u_val = upgraded[i][2]
            hp_u = str(hp_u_val)
            cost_u = str(cost_u_val) if cost_u_val > 0 else "N/A"
            choice_map[key_u] = (unit_n_str, float(hp_u_val), int(cost_u_val))
        
        if i > 0:
            table.add_row("---", "---", "---", "---", "---", "---", "---", "---", style="dim")

        unit_n_styled = Text(unit_n_str, style=faction_color) if unit_n_str else ""
        unit_u_styled = Text(unit_u_str, style=faction_color) if unit_u_str else ""

        table.add_row(f"[{key_n}]", unit_n_styled, hp_n, cost_n, f"[{key_u}]", unit_u_styled, hp_u, cost_u)
        
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


def display_game_summary(game_name: str, summary_data: list):
    """Displays the log summary for a game."""
    
    table = Table(title=f"Game Summary: '{game_name}'", border_style="green", padding=(0, 1))
    table.add_column("Unit", style="cyan", min_width=20)
    table.add_column("Total Count", style="magenta", justify="right")
    table.add_column("Demons Gained", style="green", justify="right")
    table.add_column("Wasted HP", style="red", justify="right")

    if not summary_data:
        console.print(Panel(f"[yellow]No logs found for game '{game_name}'.[/yellow]", title="Empty Summary"))
        return

    total_units = 0
    total_demons = 0
    total_waste = 0

    for row in summary_data:
        table.add_row(
            row['unit_name'],
            f"{row['total_units_ground']:.0f}",
            f"{row['total_demons_gained']:.2f}",
            f"{row['total_hp_wasted']:.2f}"
        )
        total_units += row['total_units_ground']
        total_demons += row['total_demons_gained']
        total_waste += row['total_hp_wasted']
    
    table.add_section()
    table.add_row(
        "[bold]TOTAL[/bold]",
        f"[bold magenta]{total_units:.0f}[/bold magenta]",
        f"[bold green]{total_demons:.2f}[/bold green]",
        f"[bold red]{total_waste:.2f}[/bold red]"
    )
    
    console.print(table)

def display_reverse_results(results: dict, unit_name: str):
    """Displays the results for the Reverse Calculator."""
    
    economics_section = ""
    if results['total_gold_cost'] > 0:
        gold_per_demon = results['gold_per_demon']
        profit_loss_line = ""
        if gold_per_demon > 0:
            profit_loss = DEMON_GOLD_COST - gold_per_demon
            if profit_loss > 0:
                profit_loss_line = f"    └─ Profit vs Buying:  [bold green]+{profit_loss:,.0f} gold / demon[/bold green]\n"
            else:
                profit_loss_line = f"    └─ Loss vs Buying:    [bold red]{profit_loss:,.0f} gold / demon[/bold red]\n"

        economics_section = (
            f"\n"
            f"  [bold]ECONOMICS[/bold]\n"
            f"    ├─ Total Stack Cost:[yellow]{results['total_gold_cost']:,.0f} gold[/yellow]\n"
            f"    ├─ Cost per Demon:  [bold yellow]{results['gold_per_demon']:,.0f} gold[/bold yellow]\n"
            f"{profit_loss_line}"
        )

    console.print(Panel(
        f"  [bold]TARGET[/bold]\n"
        f"    └─ Desired Demons:  [green]{results['target_demons']}[/green]\n"
        f"\n"
        f"  [bold]REQUIREMENTS[/bold]\n"
        f"    ├─ Unit to Sacrifice: [cyan]{unit_name}[/cyan] (HP: {results['unit_hp']})\n"
        f"    ├─ [bold]Units Needed:    [green]{results['needed_units']}[/green]\n"
        f"    └─ [bold]Pit Lords Needed: [green]{results['needed_pit_lords']}[/green]\n"
        f"\n"
        f"  [bold]YIELD & WASTE[/bold]\n"
        f"    ├─ Actual HP Pool:    {results['actual_hp_pool']:,.0f}\n"
        f"    ├─ Actual Demons:     [yellow]{results['actual_demons_yield']:.2f}[/yellow]\n"
        f"    └─ Wasted HP:         [red]{results['wasted_hp']:.2f}[/red] (remainder)"
        f"{economics_section}",
        title="Reverse Calculator Results",
        border_style="cyan",
        padding=1
    ))