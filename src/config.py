from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


DB_FILE_NAME = "demonic_calc.db"
DB_FILE_PATH = BASE_DIR / DB_FILE_NAME
DB_CONNECTION_STRING = f"sqlite:///{DB_FILE_PATH}"

DEMON_HP = 35
PIT_LORD_GRIND_RATE = 50


FACTION_COLORS = {
    "Zamek": "bold white",
    "Bastion": "bold green",
    "Forteca": "bold blue",
    "Inferno": "bold red",
    "Nekropolia": "grey50",
    "Lochy": "bold magenta",
    "Twierdza": "bold #D2691E", # (SaddleBrown)
    "Fort": "bold green",
    "Wrota Żywiołów": "bold cyan",
    "Przystań": "bold sea_green3",
    "Fabryka": "bold yellow3",
    "Neutralne": "dim"
}