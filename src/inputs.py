import questionary
from rich.console import Console

console = Console()

def get_string_input(prompt: str, default: str = "") -> str:
    """Safely gets a non-empty string from the user."""
    while True:
        answer = questionary.text(prompt, default=default).ask()
        if answer and answer.strip():
            return answer.strip()
        console.print("[bold red]Error: Please enter a value.[/bold red]")

def get_int_input(prompt: str, default: str = "") -> int:
    """Safely gets an integer from the user using questionary."""
    while True:
        answer = questionary.text(prompt, default=default).ask()
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