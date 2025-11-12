from sqlalchemy import create_engine, text
import datetime
from src.config import DB_CONNECTION_STRING 
from tqdm import tqdm

engine = create_engine(DB_CONNECTION_STRING)

def create_table_units():
    """Creates the 'units' table if it doesn't exist."""
    with engine.connect() as con:
        con.execute(text("""
            CREATE TABLE IF NOT EXISTS units (
                unit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                faction TEXT NOT NULL,
                unit_name TEXT NOT NULL UNIQUE,
                hp FLOAT NOT NULL, 
                is_upgraded BOOLEAN NOT NULL,
                gold_cost INTEGER NOT NULL DEFAULT 0
            );
        """))
        con.commit()

def create_table_artifacts():
    """Creates the 'artifacts' table if it doesn't exist."""
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
    """
    Creates the 'games' table if it doesn't exist.
    This table stores game-specific stats like Pit Lord count and First Aid level.
    """
    with engine.connect() as con:
        con.execute(text("""
            CREATE TABLE IF NOT EXISTS games (
                game_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                created_at DATETIME NOT NULL,
                pit_lord_count INTEGER NOT NULL DEFAULT 0,
                first_aid_level INTEGER NOT NULL DEFAULT 0
            );
        """))
        con.commit()

def create_table_game_artifacts():
    """Creates the 'game_artifacts' junction table if it doesn't exist."""
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
    """Creates the 'calculation_logs' table if it doesn't exist."""
    with engine.connect() as con:
        con.execute(text("""
            CREATE TABLE IF NOT EXISTS calculation_logs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id_fk INTEGER NOT NULL,
                timestamp DATETIME NOT NULL,
                unit_name TEXT NOT NULL,
                unit_hp_base FLOAT NOT NULL,
                unit_hp_modified FLOAT NOT NULL,
                unit_count_input INTEGER NOT NULL,
                pit_lord_input INTEGER NOT NULL,
                demons_gained FLOAT NOT NULL,
                wasted_hp FLOAT NOT NULL,
                FOREIGN KEY (game_id_fk) REFERENCES games (game_id)
                    ON DELETE CASCADE
            );
        """))
        con.commit()

def import_units():
    """
    Imports the master list of units into the 'units' table.
    Now includes gold_cost.
    """
    unit_list = [
            # Faction, Name, HP, IsUpgraded, GoldCost
            # Zamek
            ('Zamek', 'Pikinier', 10, 0, 60),
            ('Zamek', 'Halabardnik', 10, 1, 75),
            ('Zamek', 'Łucznik', 10, 0, 100),
            ('Zamek', 'Strzelec', 10, 1, 150),
            ('Zamek', 'Gryf', 25, 0, 240),
            ('Zamek', 'Królewski Gryf', 25, 1, 270),
            ('Zamek', 'Szermierz', 35, 0, 300),
            ('Zamek', 'Krzyżowiec', 35, 1, 400),
            ('Zamek', 'Mnich', 30, 0, 400),
            ('Zamek', 'Kapłan', 30, 1, 450),
            ('Zamek', 'Kawalerzysta', 100, 0, 1000),
            ('Zamek', 'Czempion', 100, 1, 1200),
            ('Zamek', 'Anioł', 200, 0, 3000),
            ('Zamek', 'Archanioł', 200, 1, 5000),

            # Bastion
            ('Bastion', 'Centaur', 8, 0, 70),
            ('Bastion', 'Kapitan Centaurów', 10, 1, 90),
            ('Bastion', 'Krasnolud', 20, 0, 130),
            ('Bastion', 'Krasnoludzki Wojownik', 20, 1, 165),
            ('Bastion', 'Leśny Elf', 15, 0, 200),
            ('Bastion', 'Wielki Elf', 15, 1, 225),
            ('Bastion', 'Pegaz', 30, 0, 350),
            ('Bastion', 'Srebrny Pegaz', 30, 1, 375),
            ('Bastion', 'Dendroid', 55, 0, 350),
            ('Bastion', 'Dendroid Strażnik', 65, 1, 425),
            ('Bastion', 'Jednorożec', 90, 0, 800),
            ('Bastion', 'Jednorożec Bitewny', 110, 1, 950),
            ('Bastion', 'Zielony Smok', 180, 0, 2400),
            ('Bastion', 'Złoty Smok', 180, 1, 4000),

            # Forteca
            ('Forteca', 'Gremiln', 4, 0, 40),
            ('Forteca', 'Mistrz Gremilnów', 4, 1, 50),
            ('Forteca', 'Kamienny Gargulec', 16, 0, 130),
            ('Forteca', 'Obsydianowy Gargulec', 16, 1, 160),
            ('Forteca', 'Kamienny Golem', 30, 0, 300),
            ('Forteca', 'Żelazny Golem', 35, 1, 350),
            ('Forteca', 'Mag', 25, 0, 350),
            ('Forteca', 'Arcymag', 30, 1, 450),
            ('Forteca', 'Dżin', 40, 0, 550),
            ('Forteca', 'Mistrz Dżinów', 40, 1, 600),
            ('Forteca', 'Naga', 110, 0, 1100),
            ('Forteca', 'Królewska Naga', 110, 1, 1600),
            ('Forteca', 'Gigant', 150, 0, 2000),
            ('Forteca', 'Tytan', 300, 1, 5000),

            # Inferno
            ('Inferno', 'Imp', 4, 0, 50),
            ('Inferno', 'Chochlik', 4, 1, 60),
            ('Inferno', 'Gog', 13, 0, 125),
            ('Inferno', 'Magog', 13, 1, 175),
            ('Inferno', 'Piekielny Ogar', 25, 0, 200),
            ('Inferno', 'Cerber', 25, 1, 250),
            ('Inferno', 'Demon', 35, 0, 250),
            ('Inferno', 'Rogaty Demon', 40, 1, 270),
            ('Inferno', 'Diablik', 90, 0, 500),
            ('Inferno', 'Arcydiablik', 90, 1, 575),
            ('Inferno', 'Efreet', 90, 0, 900),
            ('Inferno', 'Sułtański Efreet', 90, 1, 1200),
            ('Inferno', 'Diabeł', 160, 0, 2700),
            ('Inferno', 'ArcyDiabeł', 160, 1, 4500),

            # Nekropolia
            ('Nekropolia', 'Szkielet', 6, 0, 60),
            ('Nekropolia', 'Szkielet Wojownik', 6, 1, 70),
            ('Nekropolia', 'Zombie', 15, 0, 100),
            ('Nekropolia', 'Plugawy Zombie', 20, 1, 125),
            ('Nekropolia', 'Upiór', 18, 0, 200),
            ('Nekropolia', 'Zjawa', 18, 1, 230),
            ('Nekropolia', 'Wampir', 30, 0, 360),
            ('Nekropolia', 'Wampirzy Lord', 40, 1, 500),
            ('Nekropolia', 'Lisz', 30, 0, 550),
            ('Nekropolia', 'Arcylisz', 30, 1, 650),
            ('Nekropolia', 'Czarny Rycerz', 120, 0, 1200),
            ('Nekropolia', 'Mroczny Rycerz', 120, 1, 1500),
            ('Nekropolia', 'Kościany Smok', 150, 0, 1800),
            ('Nekropolia', 'Upiorny Smok', 150, 1, 3000),

            # Lochy
            ('Lochy', 'Troglodyta', 5, 0, 50),
            ('Lochy', 'Piekielny Troglodyta', 6, 1, 65),
            ('Lochy', 'Harpia', 14, 0, 130),
            ('Lochy', 'Harpia Wiedźma', 14, 1, 170),
            ('Lochy', 'Beholder', 22, 0, 260),
            ('Lochy', 'Złe Oko', 22, 1, 285),
            ('Lochy', 'Meduza', 25, 0, 300),
            ('Lochy', 'Meduza Królewska', 30, 1, 330),
            ('Lochy', 'Minotaur', 50, 0, 500),
            ('Lochy', 'Minotaur Królewski', 50, 1, 575),
            ('Lochy', 'Mantikora', 80, 0, 850),
            ('Lochy', 'Skorpikora', 80, 1, 1050),
            ('Lochy', 'Czerwony Smok', 180, 0, 2500),
            ('Lochy', 'Czarny Smok', 300, 1, 4700),

            # Twierdza
            ('Twierdza', 'Goblin', 5, 0, 40),
            ('Twierdza', 'Hobgoblin', 5, 1, 50),
            ('Twierdza', 'Wilczy Jeździec', 10, 0, 100),
            ('Twierdza', 'Wilczy Grabieżca', 10, 1, 140),
            ('Twierdza', 'Ork', 15, 0, 150),
            ('Twierdza', 'Ork Herszt', 20, 1, 190),
            ('Twierdza', 'Ogr', 40, 0, 300),
            ('Twierdza', 'Ogr Szaman', 60, 1, 450),
            ('Twierdza', 'Rok', 60, 0, 600),
            ('Twierdza', 'Ptak Gromu', 60, 1, 700),
            ('Twierdza', 'Cyklop', 70, 0, 750),
            ('Twierdza', 'Król Cyklopów', 70, 1, 1100),
            ('Twierdza', 'Behemot', 150, 0, 1500),
            ('Twierdza', 'Pradawny Behemot', 300, 1, 3000),

            # Fort
            ('Fort', 'Gnol', 6, 0, 50),
            ('Fort', 'Gnol Grabieżca', 6, 1, 70),
            ('Fort', 'Jaszczuroczłek', 14, 0, 110),
            ('Fort', 'Jaszczurzy Wojownik', 15, 1, 140),
            ('Fort', 'Ważka', 20, 0, 220),
            ('Fort', 'Ognista Ważka', 20, 1, 280),
            ('Fort', 'Bazyliszek', 35, 0, 325),
            ('Fort', 'Większy Bazyliszek', 35, 1, 400),
            ('Fort', 'Gorgona', 70, 0, 525),
            ('Fort', 'Potężna Gorgona', 70, 1, 650),
            ('Fort', 'Wiwerna', 110, 0, 800),
            ('Fort', 'Wiwerna Królewska', 110, 1, 1200),
            ('Fort', 'Hydra', 80, 0, 2200),
            ('Fort', 'Hydra Chaosu', 100, 1, 3500),

            # Wrota Żywiołów
            ('Wrota Żywiołów', 'Wróżka', 3, 0, 25),
            ('Wrota Żywiołów', 'Duszek', 3, 1, 30),
            ('Wrota Żywiołów', 'Żywiołak Powietrza', 25, 0, 250),
            ('Wrota Żywiołów', 'Żywiołak Burzy', 25, 1, 275),
            ('Wrota Żywiołów', 'Żywiołak Wody', 30, 0, 300),
            ('Wrota Żywiołów', 'Żywiołak Lodu', 30, 1, 325),
            ('Wrota Żywiołów', 'Żywiołak Ognia', 35, 0, 350),
            ('Wrota Żywiołów', 'Żywiołak Energii', 35, 1, 400),
            ('Wrota Żywiołów', 'Żywiołak Ziemi', 40, 0, 400),
            ('Wrota Żywiołów', 'Żywiołak Magmy', 40, 1, 450),
            ('Wrota Żywiołów', 'Żywiołak Psychiczny', 75, 0, 750),
            ('Wrota Żywiołów', 'Żywiołak Magii', 75, 1, 850),
            ('Wrota Żywiołów', 'Ognisty Ptak', 150, 0, 2000),
            ('Wrota Żywiołów', 'Feniks', 200, 1, 2000),

            # Przystań (Cove)
            ('Przystań', 'Nimfa', 15, 0, 130),
            ('Przystań', 'Okeanida', 16, 1, 150),
            ('Przystań', 'Mat', 20, 0, 200),
            ('Przystań', 'Bosman', 20, 1, 250),
            ('Przystań', 'Pirat', 40, 0, 325),
            ('Przystań', 'Korsarz', 40, 1, 425),
            ('Przystań', 'Ptak Morski', 45, 0, 475),
            ('Przystań', 'Ayssyda', 45, 1, 550),
            ('Przystań', 'Wiedźma Morska', 50, 0, 600),
            ('Przystań', 'Czarodziejka', 50, 1, 700),
            ('Przystań', 'Nix', 100, 0, 1100),
            ('Przystań', 'Nix Wojownik', 110, 1, 1300),
            ('Przystań', 'Wąż Morski', 280, 0, 2800),
            ('Przystań', 'Haspid', 280, 1, 5000),

            # Fabryka (Factory)
            ('Fabryka', 'Niziołek (fabryka)', 12, 0, 60),
            ('Fabryka', 'Niziołek Grenadier', 12, 1, 80),
            ('Fabryka', 'Mechanik', 30, 0, 250),
            ('Fabryka', 'Inżynier', 30, 1, 300),
            ('Fabryka', 'Pancernik', 45, 0, 400),
            ('Fabryka', 'Pancernik Hetman', 45, 1, 450),
            ('Fabryka', 'Automat', 120, 0, 1500),
            ('Fabryka', 'Strażnik Automat', 120, 1, 2000),
            ('Fabryka', 'Czerw Pustyni', 100, 0, 900),
            ('Fabryka', 'Olgoj-chorchoj', 100, 1, 1300),
            ('Fabryka', 'Rewolwerowiec', 110, 0, 1200),
            ('Fabryka', 'Łowca Nagród', 110, 1, 1700),
            ('Fabryka', 'Kuroliszek', 250, 0, 2500),
            ('Fabryka', 'Karmazynowy Kuroliszek', 250, 1, 4000),

            # Neutralne
            ('Neutralne', 'Chłop', 1, 0, 10),
            ('Neutralne', 'Niziołek', 4, 0, 20), 
            ('Neutralne', 'Duch', 8, 0, 0), # Special
            ('Neutralne', 'Zbir', 10, 0, 0), # Special
            ('Neutralne', 'Bandyta', 10, 0, 0), # Special
            ('Neutralne', 'Dzik', 15, 0, 0), # Special
            ('Neutralne', 'Koczownik', 30, 0, 0), # Special
            ('Neutralne', 'Mumia', 30, 0, 0), # Special
            ('Neutralne', 'Zaklinacz', 30, 0, 0), # Special
            ('Neutralne', 'Troll', 40, 0, 0), # Special
            ('Neutralne', 'Rdzawy Smok', 750, 0, 0), # Special
            ('Neutralne', 'Kryształowy Smok', 800, 0, 0), # Special
            ('Neutralne', 'Czarodziejski Smok', 1000, 0, 0), # Special
            ('Neutralne', 'Lazurowy Smok', 1000, 0, 0) # Special
]
    query = text("""
        INSERT INTO units (faction, unit_name, hp, is_upgraded, gold_cost) 
        VALUES (:faction, :unit_name, :hp, :is_upgraded, :gold_cost)
        ON CONFLICT(unit_name) DO UPDATE SET
            faction = excluded.faction,
            hp = excluded.hp,
            is_upgraded = excluded.is_upgraded,
            gold_cost = excluded.gold_cost
    """)

    data_to_insert = []
    for item in unit_list:
        data_to_insert.append({
            "faction": item[0],
            "unit_name": item[1],
            "hp": item[2],
            "is_upgraded": (item[3]),
            "gold_cost": item[4]
        })

    try:
        with engine.connect() as con:
            con.execute(query, data_to_insert)
            con.commit()
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
        ('Elixir of Life', 2),
    ]

    if not artifact_list:
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
    except Exception as e:
        print(f"      └─ [✖] Error inserting artifacts: {e}")

def get_factions() -> list:
    """Fetches a unique, sorted list of factions."""
    with engine.connect() as con:
        query = text("SELECT DISTINCT faction FROM units ORDER BY faction")
        result = con.execute(query)
        factions = [row[0] for row in result.fetchall()]
        return factions

def get_units_by_faction(faction: str, is_upgraded: bool) -> list:
    """Fetches units for a specific faction and upgrade status."""
    with engine.connect() as con:
        query = text("""
            SELECT unit_name, hp, gold_cost FROM units 
            WHERE faction = :faction AND is_upgraded = :is_upgraded
            ORDER BY hp
        """)
        params = {"faction": faction, "is_upgraded": is_upgraded}
        result = con.execute(query, params)
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
    Runs the full setup: creates all tables (if they don't exist) 
    and populates them with data (if missing).
    Shows a progress bar during this process.
    """
    tasks = [
        (create_table_units, "Creating 'units' table"),
        (import_units, "Importing units"),
        (create_table_artifacts, "Creating 'artifacts' table"),
        (import_artifacts, "Importing artifacts"),
        (create_table_games, "Creating 'games' table"),
        (create_table_game_artifacts, "Creating 'game_artifacts' table"),
        (create_table_logs, "Creating 'calculation_logs' table")
    ]

    print("  Checking and initializing database...")
    
    with tqdm(total=len(tasks), desc="Initialization progress", unit="step") as pbar:
        for func, description in tasks:
            pbar.set_description(f"Progress: {description}")
            func()
            pbar.update(1)

    print("  └─ [✓] Database is ready.")

def get_or_create_game(game_name: str) -> dict:
    """
    Tries to find a game by name. If it doesn't exist, creates it.
    Returns the full game row as a dictionary.
    """
    with engine.connect() as con:
        query = text("SELECT * FROM games WHERE name = :name")
        result = con.execute(query, {"name": game_name}).fetchone()
        
        if result:
            return dict(result._mapping)
        else:
            insert_query = text("""
                INSERT INTO games (name, created_at, pit_lord_count, first_aid_level)
                VALUES (:name, :created_at, 0, 0)
                RETURNING *
            """)
            params = {"name": game_name, "created_at": datetime.datetime.now()}
            new_result = con.execute(insert_query, params).fetchone()
            con.commit()
            return dict(new_result._mapping)

def update_game_stats(game_id: int, pit_lords: int, first_aid: int):
    """Updates the Pit Lord count and First Aid level for a game."""
    with engine.connect() as con:
        query = text("""
            UPDATE games 
            SET pit_lord_count = :pit_lords, first_aid_level = :first_aid
            WHERE game_id = :game_id
        """)
        con.execute(query, {"pit_lords": pit_lords, "first_aid": first_aid, "game_id": game_id})
        con.commit()

def get_game_artifacts(game_id: int) -> list:
    """Fetches a list of artifact_ids that the game currently has."""
    with engine.connect() as con:
        query = text("SELECT artifact_id_fk FROM game_artifacts WHERE game_id_fk = :game_id")
        result = con.execute(query, {"game_id": game_id})
        return [row[0] for row in result.fetchall()]

def get_all_artifacts() -> list:
    """Fetches all artifacts from the master list."""
    with engine.connect() as con:
        query = text("SELECT * FROM artifacts ORDER BY hp_bonus, name")
        result = con.execute(query)
        return [dict(row._mapping) for row in result.fetchall()]

def set_game_artifacts(game_id: int, artifact_ids: list):
    """
    Sets the complete list of artifacts for a game.
    Deletes old ones, inserts new ones.
    """
    with engine.connect() as con:
        con.execute(text("DELETE FROM game_artifacts WHERE game_id_fk = :game_id"), {"game_id": game_id})
        
        if artifact_ids:
            data_to_insert = [{"game_id_fk": game_id, "artifact_id_fk": a_id} for a_id in artifact_ids]
            con.execute(text("""
                INSERT INTO game_artifacts (game_id_fk, artifact_id_fk)
                VALUES (:game_id_fk, :artifact_id_fk)
            """), data_to_insert)
        
        con.commit()

def get_game_hp_bonus(game_id: int) -> int:
    """Calculates the total HP bonus from all of a game's artifacts."""
    with engine.connect() as con:
        query = text("""
            SELECT SUM(a.hp_bonus)
            FROM artifacts a
            JOIN game_artifacts ga ON a.artifact_id = ga.artifact_id_fk
            WHERE ga.game_id_fk = :game_id
        """)
        result = con.execute(query, {"game_id": game_id}).scalar()
        return result or 0

def log_calculation(game_id: int, unit_name: str, base_hp: float, mod_hp: float, count: int, pit_lords: int, demons: float, waste: float):
    """Logs a single farming calculation to the database."""
    with engine.connect() as con:
        query = text("""
            INSERT INTO calculation_logs (
                game_id_fk, timestamp, unit_name, unit_hp_base, unit_hp_modified,
                unit_count_input, pit_lord_input, demons_gained, wasted_hp
            ) VALUES (
                :game_id_fk, :timestamp, :unit_name, :unit_hp_base, :unit_hp_modified,
                :unit_count_input, :pit_lord_input, :demons_gained, :wasted_hp
            )
        """)
        params = {
            "game_id_fk": game_id,
            "timestamp": datetime.datetime.now(),
            "unit_name": unit_name,
            "unit_hp_base": base_hp,
            "unit_hp_modified": mod_hp,
            "unit_count_input": count,
            "pit_lord_input": pit_lords,
            "demons_gained": demons,
            "wasted_hp": waste
        }
        con.execute(query, params)
        con.commit()

def get_game_log_summary(game_id: int) -> list:
    """
    Fetches all logs for a game and groups them by unit name,
    summing up the totals.
    """
    with engine.connect() as con:
        query = text("""
            SELECT
                unit_name,
                SUM(unit_count_input) AS total_units_ground,
                SUM(demons_gained) AS total_demons_gained,
                SUM(wasted_hp) AS total_hp_wasted
            FROM calculation_logs
            WHERE game_id_fk = :game_id
            GROUP BY unit_name
            ORDER BY total_demons_gained DESC
        """)
        result = con.execute(query, {"game_id": game_id})
        return [dict(row._mapping) for row in result.fetchall()]

def get_all_games() -> list:
    """Fetches all existing games, ordered by name."""
    with engine.connect() as con:
        query = text("SELECT game_id, name, created_at FROM games ORDER BY name")
        rows = con.execute(query).fetchall()
        
        games_list = []
        for row in rows:
            game_data = dict(row._mapping)
            
            if isinstance(game_data['created_at'], str):
                try:
                    game_data['created_at'] = datetime.datetime.fromisoformat(game_data['created_at'])
                except ValueError:
                    game_data['created_at'] = datetime.datetime.strptime(game_data['created_at'], '%Y-%m-%d %H:%M:%S')
            
            games_list.append(game_data)
            
        return games_list

def delete_game(game_id: int):
    """Deletes a game and all its associated logs/artifacts."""
    with engine.connect() as con:
        query = text("DELETE FROM games WHERE game_id = :game_id")
        con.execute(query, {"game_id": game_id})
        con.commit()