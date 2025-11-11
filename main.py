import src.cli as cli
import src.db as db
from sqlalchemy.exc import OperationalError


print(f"--- DEBUG: Ścieżka używana przez silnik: {db.engine.url}")

def main():
    print("Initializing database...")
    db.initialize_database()
    print("Database is ready.")
    cli.start_app()


if __name__ == "__main__":
    main() 
    



