# 🔥 HotA Demon Farming Calculator 🔥

Because if you're not min-maxing your demon farming in a 25-year-old game, are you even playing it right?
Yeah, I'm the life of the party. What about it?

Welcome to the advanced calculator for **Heroes of Might & Magic 3: Horn of the Abyss (HotA)**. This CLI (Command-Line Interface) tool answers all your burning questions about Pit Lords and helps you maximize your gains.

## 🌟 What's Inside? (What it does)

* **Game Mode:** Create and load saved "games." The app remembers your *First Aid* level, equipped *HP Artifacts*, and your default Pit Lord count.
* **Full HotA Database:** All units from all factions (including Cove and Factory) complete with their **Gold Cost**. Yes, I manually entered all of them. You're welcome.
* **Standard Calculator:** Simple calculations for "how many units give how many demons?".
* **Reverse Calculator:** Enter how many demons you want, and the app tells you how many units and Pit Lords you need. Because "I *think* this is enough" is a terrible strategy.
* **Cost Analysis:** The app automatically calculates the **cost per demon** and shows whether you are **profiting or losing gold** compared to buying demons in town (for 250 gold).
* **Distribution Chart:** An interactive chart that shows the "sweet spots" (`PERFECT STACK`) for your units, so you don't waste a single HP.
* **Game Management:** Easily create, load, and **delete** your saved game profiles.

## 📸 App Demo (How it looks)

Here is a sample workflow in **Game Mode**, showing the economic analysis. Why yes, that *is* a `Loss vs Buying`. Sacrificing actual Demons to make... Demons... is a good business plan.

```text
╭──────────────────────────────────────────────╮
│        DEMON FARMING CALCULATOR (HotA)       │
╰──────────────────────────────────────────────╯
? Select option: Game Mode (Load/Create)

╭──────────────────────────────────────────────╮
│                  Game Mode                   │
│                                              │
│ Select a game to load or create a new one.   │
╰──────────────────────────────────────────────╯
? Select a game or create a new one: [ CREATE NEW GAME ]
? Enter new game name (e.g., 'my_game_02'): WePlayForFun

Loaded game: 'WePlayForFun'
──────────────── Game Mode: WePlayForFun | Pit Lords: 0 | First Aid Lvl: 0 ────────────────
? Select action: Farm Demons (Calculator)
? Select unit HP source: Select from database
? Select Faction: Inferno

╭───────────────────────────────────────────────────────────────────────────────────╮
│                             Select Unit (Inferno)                                 │
├─────┬──────────────────┬──────┬───────┬─────┬───────────────────┬──────┬───────── ┤
│ Key │ Non-Upgraded     │ HP   │ Cost  │ Key │ Upgraded          │ HP   │ Cost     │
│ [1] │ Imp              │ 4.0  │ 50    │ [11]│ Chochlik          │ 4.0  │ 60       │
│ --- │ ---              │ ---  │ ---   │ --- │ ---               │ ---  │ ---      │
│ [2] │ Gog              │ 13.0 │ 125   │ [22]│ Magog             │ 13.0 │ 175      │
│ --- │ ---              │ ---  │ ---   │ --- │ ---               │ ---  │ ---      │
│ [3] │ Piekielny Ogar   │ 25.0 │ 200   │ [33]│ Cerber            │ 25.0 │ 250      │
│ --- │ ---              │ ---  │ ---   │ --- │ ---               │ ---  │ ---      │
│ [4] │ Demon            │ 35.0 │ 250   │ [44]│ Rogaty Demon      │ 40.0 │ 270      │
│ ... │ ...              │ ...  │ ...   │ ... │ ...               │ ...  │ ...      │
╰───────────────────────────────────────────────────────────────────────────────────╯
? Enter number (or '0' to cancel/back): 4
? Number of units (Demon | Base HP: 35.0 -> Mod: 35.00): 100
? Enter number of Pit Lords (needed: 50): 50

╭──────────────────────────────────────────────────────────────────────────────────╮
│                             Calculation Results                                  │
│                                                                                  │
│    INPUT DATA                                                                    │
│      ├─ Units:           100 x (Unit: Demon)                                     │
│      ├─ Base HP:         35.0                                                    │
│      ├─ Artifact Bonus:  +0                                                      │
│      ├─ First Aid Lvl:   0 (0%)                                                  │
│      └─ Modified HP:     35.00                                                   │
│      ├─ Total HP Pool:   3,500 (from Modified HP)                                │
│      └─ Pit Lords Used:  50                                                      │
│                                                                                  │
│    YIELD                                                                         │
│      ├─ Max (from HP):   100.00                                                  │
│      ├─ Max (from Lords): 71.43                                                  │
│      └─ >>  ACTUALLY GAINED: 71.43 demons                                        │
│                                                                                  │
│    OPTIMIZATION (Based on Modified HP)                                           │
│      ├─ Wasted HP:       0.00 (remainder)                                        │
│      ├─ Needed Lords:    50 (for this stack)                                     │
│      └─ Perfect Stack:   1 units (for 35 HP)                                     │
│                                                                                  │
│    ECONOMICS                                                                     │
│      ├─ Unit Cost:       250 gold                                                │
│      ├─ Total Stack Cost:25,000 gold                                             │
│      ├─ Cost per Demon:  350 gold                                                │
│      └─ Loss vs Buying:    -100 gold / demon                                     │
│                                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────╯
```
## 🚀 Get It Running (How to Install)

This is a standalone application! You **do not** need to install Python or any libraries.

### For Linux Users:

1.  Go to the **[Releases](https://github.com/D-Kniec/homm3-demon-calculator/releases)** tab on this GitHub page.
2.  Download the latest `.zip` file (e.g., `demon-calc-linux.zip`).
3.  Unzip the file. You will get a single executable file named `demon-calc`.
4.  Open your terminal and go to the folder where you unzipped the file.
5.  **Important:** You must make the file executable first:
    ```bash
    chmod +x demon-calc
    ```
6.  Run the application:
    ```bash
    ./demon-calc
    ```

### For Windows Users:

1.  Go to the **[Releases](https://github.com/D-Kniec/homm3-demon-calculator/releases)** tab on this GitHub page.
2.  Download the latest `.zip` file (e.g., `demon-calc-windows.zip`).
3.  Unzip the file.
4.  Double-click the `demon-calc.exe` file to run the application. (Windows may show a security warning because the file is not "signed". You may need to click "More info" -> "Run anyway").

---

<details>
<summary><b>(Advanced) For Developers: How to Run from Source</b></summary>

If you want to run the app directly from the Python source code instead of using the executable.

1.  **Prerequisites:** You need [Python 3.10+](https://www.python.org/downloads/) installed.

2.  **Get the Code:**
    ```bash
    git clone [https://github.com/D-Kniec/homm3-demon-calculator.git](https://github.com/D-Kniec/homm3-demon-calculator.git)
    cd homm3-demon-calculator
    ```

3.  **Create Virtual Environment:**
    ```bash
    # On macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    
    # On Windows
    python -m venv .venv
    .\.venv\Scripts\activate
    ```

4.  **Install Dependencies:**
    ```bash
    pip install sqlalchemy rich questionary tqdm
    ```

5.  **Run the App:**
    ```bash
    python main.py
    ```
    *(The first run will auto-generate the `src/demonic_calc.db` file)*

</details>

## 🛠️ Tech Stack (aka The Nerd Stuff)

* **Python 3.10+**
* **Rich:** For beautiful CLI panels, tables, and colors.
* **Questionary:** For interactive menus and prompts.
* **SQLAlchemy:** For communicating with the database.
* **tqdm:** For the one-time database initialization progress bar.
* **SQLite:** Because a full-blown PostgreSQL database would be *slight* overkill.
'''

## 📂 Project Structure

Here's how the code is organized:
* **`demon-calc/`** (Main project root)
    * **`.venv/`**: Virtual environment folder (ignored)
    * **`src/`**: Main source code folder
        * `cli.py`: Main application logic and menus (controller)
        * `config.py`: Constants (Demon HP, cost, DB path)
        * `core.py`: All the math (the "brain")
        * `db.py`: Database logic (data management)
        * `inputs.py`: User prompt handling
        * `views.py`: Table and panel display (the "face")
        * `demonic_calc.db`: (Auto-generated) SQLite database
    * **`main.py`**: The application's entry point
    * **`README.md`**: This file