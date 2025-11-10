import src.cli as cli
import src.db as db
from sqlalchemy.exc import OperationalError


print(f"--- DEBUG: Ścieżka używana przez silnik: {db.engine.url}")

def main():
    if db.get_factions()==0:
        db.initialize_database()
        print("initialization completed :] run code again...")
    else:
        cli.start_app()


if __name__ == "__main__":
    main() 
    