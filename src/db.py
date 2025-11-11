# db.py

from sqlalchemy import create_engine, text
import datetime
from src.config import DB_CONNECTION_STRING 

engine = create_engine(DB_CONNECTION_STRING)

# --- 1. DDL (Table Creation) Functions ---

def create_table_units():
    with engine.connect() as con:
        con.execute(text("""
            CREATE TABLE IF NOT EXISTS units (
                unit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                faction TEXT NOT NULL,
                unit_name TEXT NOT NULL UNIQUE,
                hp FLOAT NOT NULL, 
                is_upgraded BOOLEAN NOT NULL
            );
        """))
        con.commit()

def create_table_artifacts():
    with engine.connect() as con:
        con.execute(text("""
            CREATE TABLE IF NOT EXISTS artifacts (
                artifact_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                hp_bonus INTEGER NOT NULL DEFAULT 0
            );
        """))
        con.commit()

def create_table_games():
    with engine.connect() as con:
        con.execute(text("""
            CREATE TABLE IF NOT EXISTS games (
                game_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                created_at DATETIME NOT NULL,
                first_aid_level INTEGER NOT NULL DEFAULT 0
            );
        """))
        con.commit()

def create_table_game_artifacts():
    with engine.connect() as con:
        con.execute(text("""
            CREATE TABLE IF NOT EXISTS game_artifacts (
                game_id_fk INTEGER NOT NULL,
                artifact_id_fk INTEGER NOT NULL,
                FOREIGN KEY (game_id_fk) REFERENCES games (game_id) ON DELETE CASCADE,
                FOREIGN KEY (artifact_id_fk) REFERENCES artifacts (artifact_id) ON DELETE CASCADE,
                PRIMARY KEY (game_id_fk, artifact_id_fk)
            );
        """))
        con.commit()

def create_table_logs():
    with engine.connect() as con:
        con.execute(text("""
            CREATE TABLE IF NOT EXISTS calculation_logs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id_fk INTEGER NOT NULL,
                timestamp DATETIME NOT NULL,
                unit_name TEXT NOT NULL,
                unit_count_input INTEGER NOT NULL,
                pit_lord_input INTEGER NOT NULL,
                demons_gained INTEGER NOT NULL,
                wasted_hp FLOAT NOT NULL,
                FOREIGN KEY (game_id_fk) REFERENCES games (game_id)
                    ON DELETE CASCADE
            );
        """))
        con.commit()

# --- 2. DML (Data Population) Functions ---

def import_units():
    """
    Imports units
    """
unit_list = [
            # Zamek
            ('Zamek', 'Pikinier', 10, 0),
            ('Zamek', 'Halabardnik', 10, 1),
            ('Zamek', 'Łucznik', 10, 0),
            ('Zamek', 'Strzelec', 10, 1),
            ('Zamek', 'Gryf', 25, 0),
            ('Zamek', 'Królewski Gryf', 25, 1),
            ('Zamek', 'Szermierz', 35, 0),
            ('Zamek', 'Krzyżowiec', 35, 1),
            ('Zamek', 'Mnich', 30, 0),
            ('Zamek', 'Kapłan', 30, 1),
            ('Zamek', 'Kawalerzysta', 100, 0),
            ('Zamek', 'Czempion', 100, 1),
            ('Zamek', 'Anioł', 200, 0),
            ('Zamek', 'Archanioł', 200, 1),

            # Bastion
            ('Bastion', 'Centaur', 8, 0),
            ('Bastion', 'Kapitan Centaurów', 10, 1),
            ('Bastion', 'Krasnolud', 20, 0),
            ('Bastion', 'Krasnoludzki Wojownik', 20, 1),
            ('Bastion', 'Leśny Elf', 15, 0),
            ('Bastion', 'Wielki Elf', 15, 1),
            ('Bastion', 'Pegaz', 30, 0),
            ('Bastion', 'Srebrny Pegaz', 30, 1),
            ('Bastion', 'Dendroid', 55, 0),
            ('Bastion', 'Dendroid Strażnik', 65, 1),
            ('Bastion', 'Jednorożec', 90, 0),
            ('Bastion', 'Jednorożec Bitewny', 110, 1),
            ('Bastion', 'Zielony Smok', 180, 0),
            ('Bastion', 'Złoty Smok', 180, 1),

            # Forteca
            ('Forteca', 'Gremiln', 4, 0),
            ('Forteca', 'Mistrz Gremilnów', 4, 1),
            ('Forteca', 'Kamienny Gargulec', 16, 0),
            ('Forteca', 'Obsydianowy Gargulec', 16, 1),
            ('Forteca', 'Kamienny Golem', 30, 0),
            ('Forteca', 'Żelazny Golem', 35, 1),
            ('Forteca', 'Mag', 25, 0),
            ('Forteca', 'Arcymag', 30, 1),
            ('Forteca', 'Dżin', 40, 0),
            ('Forteca', 'Mistrz Dżinów', 40, 1),
            ('Forteca', 'Naga', 110, 0),
            ('Forteca', 'Królewska Naga', 110, 1),
            ('Forteca', 'Gigant', 150, 0),
            ('Forteca', 'Tytan', 300, 1),

            # Inferno
            ('Inferno', 'Imp', 4, 0),
            ('Inferno', 'Chochlik', 4, 1),
            ('Inferno', 'Gog', 13, 0),
            ('Inferno', 'Magog', 13, 1),
            ('Inferno', 'Piekielny Ogar', 25, 0),
            ('Inferno', 'Cerber', 25, 1),
            ('Inferno', 'Demon', 35, 0),
            ('Inferno', 'Rogaty Demon', 40, 1),
            ('Inferno', 'Diablik', 90, 0),
            ('Inferno', 'Arcydiablik', 90, 1),
            ('Inferno', 'Efreet', 90, 0),
            ('Inferno', 'Sułtański Efreet', 90, 1),
            ('Inferno', 'Diabeł', 160, 0),
            ('Inferno', 'ArcyDiabeł', 160, 1),

            # Nekropolia
            ('Nekropolia', 'Szkielet', 6, 0),
            ('Nekropolia', 'Szkielet Wojownik', 6, 1),
            ('Nekropolia', 'Zombie', 15, 0),
            ('Nekropolia', 'Plugawy Zombie', 20, 1),
            ('Nekropolia', 'Upiór', 18, 0),
            ('Nekropolia', 'Zjawa', 18, 1),
            ('Nekropolia', 'Wampir', 30, 0),
            ('Nekropolia', 'Wampirzy Lord', 40, 1),
            ('Nekropolia', 'Lisz', 30, 0),
            ('Nekropolia', 'Arcylisz', 30, 1),
            ('Nekropolia', 'Czarny Rycerz', 120, 0),
            ('Nekropolia', 'Mroczny Rycerz', 120, 1),
            ('Nekropolia', 'Kościany Smok', 150, 0),
            ('Nekropolia', 'Upiorny Smok', 150, 1),

            # Lochy
            ('Lochy', 'Troglodyta', 5, 0),
            ('Lochy', 'Piekielny Troglodyta', 6, 1),
            ('Lochy', 'Harpia', 14, 0),
            ('Lochy', 'Harpia Wiedźma', 14, 1),
            ('Lochy', 'Beholder', 22, 0),
            ('Lochy', 'Złe Oko', 22, 1),
            ('Lochy', 'Meduza', 25, 0),
            ('Lochy', 'Meduza Królewska', 30, 1),
            ('Lochy', 'Minotaur', 50, 0),
            ('Lochy', 'Minotaur Królewski', 50, 1),
            ('Lochy', 'Mantikora', 80, 0),
            ('Lochy', 'Skorpikora', 80, 1),
            ('Lochy', 'Czerwony Smok', 180, 0),
            ('Lochy', 'Czarny Smok', 300, 1),

            # Twierdza
            ('Twierdza', 'Goblin', 5, 0),
            ('Twierdza', 'Hobgoblin', 5, 1),
            ('Twierdza', 'Wilczy Jeździec', 10, 0),
            ('Twierdza', 'Wilczy Grabieżca', 10, 1),
            ('Twierdza', 'Ork', 15, 0),
            ('Twierdza', 'Ork Herszt', 20, 1),
            ('Twierdza', 'Ogr', 40, 0),
            ('Twierdza', 'Ogr Szaman', 60, 1),
            ('Twierdza', 'Rok', 60, 0),
            ('Twierdza', 'Ptak Gromu', 60, 1),
            ('Twierdza', 'Cyklop', 70, 0),
            ('Twierdza', 'Król Cyklopów', 70, 1),
            ('Twierdza', 'Behemot', 150, 0),
            ('Twierdza', 'Pradawny Behemot', 300, 1),

            # Fort
            ('Fort', 'Gnol', 6, 0),
            ('Fort', 'Gnol Grabieżca', 6, 1),
            ('Fort', 'Jaszczuroczłek', 14, 0),
            ('Fort', 'Jaszczurzy Wojownik', 15, 1),
            ('Fort', 'Ważka', 20, 0),
            ('Fort', 'Ognista Ważka', 20, 1),
            ('Fort', 'Bazyliszek', 35, 0),
            ('Fort', 'Większy Bazyliszek', 35, 1),
            ('Fort', 'Gorgona', 70, 0),
            ('Fort', 'Potężna Gorgona', 70, 1),
            ('Fort', 'Wiwerna', 110, 0),
            ('Fort', 'Wiwerna Królewska', 110, 1),
            ('Fort', 'Hydra', 80, 0),
            ('Fort', 'Hydra Chaosu', 100, 1),

            # Wrota Żywiołów
            ('Wrota Żywiołów', 'Wróżka', 3, 0),
            ('Wrota Żywiołów', 'Duszek', 3, 1),
            ('Wrota Żywiołów', 'Żywiołak Powietrza', 25, 0),
            ('Wrota Żywiołów', 'Żywiołak Burzy', 25, 1),
            ('Wrota Żywiołów', 'Żywiołak Wody', 30, 0),
            ('Wrota Żywiołów', 'Żywiołak Lodu', 30, 1),
            ('Wrota Żywiołów', 'Żywiołak Ognia', 35, 0),
            ('Wrota Żywiołów', 'Żywiołak Energii', 35, 1),
            ('Wrota Żywiołów', 'Żywiołak Ziemi', 40, 0),
            ('Wrota Żywiołów', 'Żywiołak Magmy', 40, 1),
            ('Wrota Żywiołów', 'Żywiołak Psychiczny', 75, 0),
            ('Wrota Żywiołów', 'Żywiołak Magii', 75, 1),
            ('Wrota Żywiołów', 'Ognisty Ptak', 150, 0),
            ('Wrota Żywiołów', 'Feniks', 200, 1),

            # Przystań (Cove)
            ('Przystań', 'Nimfa', 15, 0),
            ('Przystań', 'Okeanida', 16, 1),
            ('Przystań', 'Mat', 20, 0),
            ('Przystań', 'Bosman', 20, 1),
            ('Przystań', 'Pirat', 40, 0),
            ('Przystań', 'Korsarz', 40, 1),
            ('Przystań', 'Ptak Morski', 45, 0),
            ('Przystań', 'Ayssyda', 45, 1),
            ('Przystań', 'Wiedźma Morska', 50, 0),
            ('Przystań', 'Czarodziejka', 50, 1),
            ('Przystań', 'Nix', 100, 0),
            ('Przystań', 'Nix Wojownik', 110, 1),
            ('Przystań', 'Wąż Morski', 280, 0),
            ('Przystań', 'Haspid', 280, 1),

            # Fabryka (Factory)
            ('Fabryka', 'Niziołek (fabryka)', 12, 0),
            ('Fabryka', 'Niziołek Grenadier', 12, 1),
            ('Fabryka', 'Mechanik', 30, 0),
            ('Fabryka', 'Inżynier', 30, 1),
            ('Fabryka', 'Pancernik', 45, 0),
            ('Fabryka', 'Pancernik Hetman', 45, 1),
            ('Fabryka', 'Automat', 120, 0),
            ('Fabryka', 'Strażnik Automat', 120, 1),
            ('Fabryka', 'Czerw Pustyni', 100, 0),
            ('Fabryka', 'Olgoj-chorchoj', 100, 1),
            ('Fabryka', 'Rewolwerowiec', 110, 0),
            ('Fabryka', 'Łowca Nagród', 110, 1),
            ('Fabryka', 'Kuroliszek', 250, 0),
            ('Fabryka', 'Karmazynowy Kuroliszek', 250, 1),

            # Neutralne
            ('Neutralne', 'Chłop', 1, 0),
            ('Neutralne', 'Niziołek', 4, 0), 
            ('Neutralne', 'Duch', 8, 0),
            ('Neutralne', 'Zbir', 10, 0),
            ('Neutralne', 'Bandyta', 10, 0),
            ('Neutralne', 'Dzik', 15, 0),
            ('Neutralne', 'Koczownik', 30, 0),
            ('Neutralne', 'Mumia', 30, 0),
            ('Neutralne', 'Zaklinacz', 30, 0),
            ('Neutralne', 'Troll', 40, 0),
            ('Neutralne', 'Rdzawy Smok', 750, 0),
            ('Neutralne', 'Kryształowy Smok', 800, 0),
            ('Neutralne', 'Czarodziejski Smok', 1000, 0),
            ('Neutralne', 'Lazurowy Smok', 1000, 0)
]
    query = text("""
        INSERT INTO units (faction, unit_name, hp, is_upgraded) 
        VALUES (:faction, :unit_name, :hp, :is_upgraded)
        ON CONFLICT(unit_name) DO NOTHING
    """)

    data_to_insert = []
    for item in unit_list:
        data_to_insert.append({
            "faction": item[0],
            "unit_name": item[1],
            "hp": item[2],
            "is_upgraded": (item[3])
        })

    try:
        with engine.connect() as con:
            con.execute(query, data_to_insert)
            con.commit()
        
        print(f"      └─ [✓] Successfully processed {len(data_to_insert)} units.")
    except Exception as e:
        print(f"      └─ [✖] Error inserting units: {e}")

def import_artifacts():
    """
    Imports HP-boosting artifacts (master list) into the 'artifacts' table.
    """
    artifact_list = [
        ('Vial of Lifeblood', 1),
        ('Ring of Vitality', 1),
        ('Ring of Life', 1),
    ]

    if not artifact_list:
        print("    └─ [✓] Skipping artifacts (no data to import).")
        return

    query = text("""
        INSERT INTO artifacts (name, hp_bonus) 
        VALUES (:name, :hp_bonus)
        ON CONFLICT(name) DO NOTHING
    """)
    
    data_to_insert = []
    for item in artifact_list:
        data_to_insert.append({
            "name": item[0],
            "hp_bonus": item[1]
        })

    try:
        with engine.connect() as con:
            con.execute(query, data_to_insert)
            con.commit()
        
        print(f"      └─ [✓] Successfully processed {len(data_to_insert)} artifacts.")
    except Exception as e:
        print(f"      └─ [✖] Error inserting artifacts: {e}")


# --- 3. DQL (Data Query) Functions (Functions for cli.py) ---

def get_factions() -> list:
    """Fetches a unique, sorted list of factions."""
    try:
        with engine.connect() as con:
            query = text("SELECT DISTINCT faction FROM units ORDER BY faction")
            result = con.execute(query)
            factions = [row[0] for row in result.fetchall()]
            return factions
    except Exception as e:
        print(f"!!! KRYTYCZNY BŁĄD w get_factions: {e}") 
        return 0

def get_units_by_faction(faction: str, is_upgraded: bool) -> list:
    """Fetches units for a specific faction and upgrade status."""
    with engine.connect() as con:
        query = text("""
            SELECT unit_name, hp FROM units 
            WHERE faction = :faction AND is_upgraded = :is_upgraded
            ORDER BY hp
        """)
        params = {"faction": faction, "is_upgraded": is_upgraded}
        result = con.execute(query, params)
        return result.fetchall()

def get_artifacts() -> list:
    """Fetches all artifacts with their bonus."""
    with engine.connect() as con:
        query = text("SELECT artifact_id, name, hp_bonus FROM artifacts ORDER BY name")
        result = con.execute(query)
        return result.fetchall()

def get_unit_hp(unit_name: str) -> float:
    """Gets the HP for a single, specific unit."""
    with engine.connect() as con:
        query = text("SELECT hp FROM units WHERE unit_name = :unit_name")
        params = {"unit_name": unit_name}
        result = con.execute(query, params).fetchone()
        return result[0] if result else 0.0


def initialize_database():
    """
    Runs the full, first-time setup: creates all tables and populates them.
    """
    print("  Creating tables...")
    create_table_units()
    print("  ├─ [✓] 'units' table is ready.")
    import_units()
    create_table_artifacts()
    print("  ├─ [✓] 'artifacts' table is ready.")
    import_artifacts()
    create_table_games()
    print("  ├─ [✓] 'games' table is ready.")
    create_table_game_artifacts()
    print("  ├─ [✓] 'game_artifacts' (link table) is ready.")
    create_table_logs()
    print("  └─ [✓] 'calculation_logs' table is ready.")


