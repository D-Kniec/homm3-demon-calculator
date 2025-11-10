from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


DB_FILE_NAME = "demonic_calc.db"
DB_FILE_PATH = BASE_DIR / DB_FILE_NAME
DB_CONNECTION_STRING = f"sqlite:///{DB_FILE_PATH}"

DEMON_HP = 35
PIT_LORD_GRIND_RATE = 50