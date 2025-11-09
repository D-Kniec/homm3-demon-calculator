import cli
import db
from sqlalchemy.exc import OperationalError
import sys
import os

def main():
    if db.get_factions()==0:
        db.initialize_database()
        print("initialization compledted :] run code again...")
    else:
        cli.start_app()


if __name__ == "__main__":
    main()