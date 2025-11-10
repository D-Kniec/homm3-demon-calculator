# 🔥 HotA Demon Farming Calculator 🔥

This is a simple Python CLI tool to calculate and optimize your demon farming in **Heroes of Might & Magic 3: Horn of the Abyss (HotA)**.

It answers the eternal question: "How many demons will I *actually* get if I sacrifice X units with Y Pit Lords?" and helps you stop wasting precious HP.

## 🌟 What's Inside?

* **Sandbox Mode:** Just punch in a unit's HP and stack size. No fuss.
* **Full HoMM3 Database:** Don't remember the HP of a *Dendroid Strażnik*? No problem. The app has a full, built-in database of *all* units from *all* factions (including Conflux and Neutrals).
* **Full Analysis:** Tells you *exactly* what you get, what you waste, and what your bottleneck is (not enough HP or not enough Pit Lords).
* **"Perfect Stack" Solver:** Calculates the *smallest* stack of a unit needed for a 0% waste conversion.
* **Interactive Chart:** This is the cool part. It shows you a live ASCII chart of the units +/- 4 from your current stack, so you can see *exactly* where the "perfect" breakpoints are.

## 📸 Live Demo (Text-style)

Here's a sample run choosing a unit from the database.

```text
╔════════════════════════════════════════════╗
║        DEMON FARMING CALCULATOR (HotA)       ║
╠════════════════════════════════════════════╣
║ [1] Simple Calculator ('Sandbox' Mode)       ║
║ [2] Game Mode (Load/Create) (TODO)           ║
║ [0] Exit                                     ║
╚════════════════════════════════════════════╝
Select option: 1

--- Simple Calculator ---
Select unit HP source:
  [1] Select from database
  [2] Enter HP manually
  [0] Back to Main Menu
Choice: 1

--- Select Faction ---
  [1] Bastion
  [2] Fort
  [3] Forteca
  [4] Inferno
  [5] Lochy
  [6] Nekropolia
  [7] Neutralne
  [8] Twierdza
  [9] Wrota Żywiołów
  [10] Zamek
Enter number (or '0' to cancel/back): 1

--- Select Unit (Bastion) ---
  -Non-Upgraded
    ├─ [1] Centaur (HP: 8.0)
    ├─ [2] Leśny Elf (HP: 15.0)
    ...
  -Upgraded
    ├─ [8] Kapitan Centaurów (HP: 10.0)
    ...
    ├─ [12] Dendroid Strażnik (HP: 65.0)
    ...
--------------------
Enter number (or '0' to cancel/back): 12
Enter number of units (HP: 65.0): 100
Enter number of Pit Lords: 5

--- CALCULATION RESULTS ---
  Unit: 100 x (HP: 65.0)
  Total HP Pool: 6500
  Pit Lords Used: 5
--------------------
  Max demons from HP pool: 185.71
  Max demons from Pit Lords: 7.14
  ACTUALLY GAINED: 7.14 demons
--------------------
--- Optimization ---
  Wasted HP (remainder): 25.0
  Required Pit Lords for full conversion: 130
  Perfect stack (0 waste): 7 units (for 455 HP)

--- Local Distribution Chart ---
           █ = *Potential* Demons from HP (scaled to list max)
           Lords = *Theoretical* Pit Lords needed for this stack
           [✓]/[ ] = Is your 5 Pit Lords enough for THIS GROUP?

 [ ]   ? lords |  96 Units: [███████████████████████  ] 178.29 Demons | Waste:  5.0 HP
 [ ]  ?? lords | (...)
 [✓]  1 lord |   7 Units: [█                        ]  13.00 Demons | Waste:  0.0 HP <-- PERFECT STACK
 [✓]  5 lords |  98 Units: [████████████████████████ ] 182.00 Demons | Waste: 15.0 HP
 [ ]  16 lords |  99 Units: [████████████████████████ ] 183.86 Demons | Waste:  0.0 HP <-- PERFECT STACK
 [ ]  27 lords | 100 Units: [█████████████████████████] 185.71 Demons | Waste: 25.0 HP <-- CURRENT (Need +4 for PERFECTION)
 [ ]  38 lords | 101 Units: [█████████████████████████] 187.57 Demons | Waste: 15.0 HP
 [ ]  49 lords | 102 Units: [█████████████████████████] 189.43 Demons | Waste:  5.0 HP
 [ ]  61 lords | 103 Units: [█████████████████████████] 191.29 Demons | Waste: 30.0 HP
 [ ]  72 lords | 104 Units: [█████████████████████████] 193.14 Demons | Waste: 20.0 HP
 [ ] 115 lords | (...)
 [ ] 130 lords | 106 Units: [█████████████████████████] 196.86 Demons | Waste:  0.0 HP <-- PERFECT STACK

... press Enter to calculate for another unit in this faction ...
```

## 🚀 Get It Running

This thing is lightweight. You only need `SQLAlchemy`.

1.  **Clone the repo:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/YOUR_REPONAME.git](https://github.com/YOUR_USERNAME/YOUR_REPONAME.git)
    cd YOUR_REPONAME
    ```

2.  **(Recommended) Make a virtual environment:**
    ```bash
    # Linux/macOS
    python3 -m venv .venv
    source .venv/bin/activate
    
    # Windows
    python -m venv .venv
    .\.venv\Scripts\activate
    ```

3.  **Install the one (1) dependency:**
    ```bash
    pip install sqlalchemy
    ```

4.  **Run it!**
    ```bash
    python main.py
    ```

**🚨 HEY, LISTEN! (First-Time Run):**
The very first time you run it, the script will build the SQLite database (`demonic_calc.db`) and fill it with all the unit stats. It'll say `initialization completed...` and quit.

**Just run `python main.py` again.** You're good to go. (It only does this once).

## 🛠️ Tech Stuff

* **Python 3.10+**
* **SQLAlchemy:** The only non-standard library, used for talking to the database.
* **SQLite:** For the super-light, file-based database of units.

## 📂 Project Structure

Pretty clean, right?

```
demon-calc/
├── .venv/
├── src/
│   ├── __init__.py
│   ├── cli.py              # The UI (what you see)
│   ├── config.py           # Config (DB path, game constants)
│   ├── core.py             # The "brain" (all the math)
│   ├── db.py               # The "muscle" (database logic)
│   └── demonic_calc.db     # (Auto-generated database)
├── main.py                 # The entry point (runs the app)
└── README.md
```