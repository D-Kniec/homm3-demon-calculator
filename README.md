# 🔥 HotA Demon Farming Calculator 🔥

This is a Python CLI tool to calculate and optimize your demon farming in **Heroes of Might & Magic 3: Horn of the Abyss (HotA)**.

It answers the eternal question: "How many demons will I *actually* get if I sacrifice X units with Y Pit Lords?" and helps you stop wasting precious HP.

This version uses the `rich` and `questionary` libraries for a modern, interactive, and colorful UI.

## 🌟 What's Inside?

* **Sandbox Mode:** Just punch in a unit's HP and stack size. No fuss.
* **Full HoMM3 Database:** Don't remember the HP of a *Dendroid Strażnik*? No problem. The app has a full, built-in database of *all* units from *all* factions (including **Cove, Factory, Conflux, and Neutrals**).
* **Full Analysis:** Tells you *exactly* what you get, what you waste, and what your bottleneck is (not enough HP or not enough Pit Lords).
* **"Perfect Stack" Solver:** Calculates the *smallest* stack of a unit needed for a 0% waste conversion.
* **Interactive Chart:** This is the cool part. It shows you a live, richly-formatted chart of the units +/- 4 from your current stack, so you can see *exactly* where the "perfect" breakpoints are.

## 📸 Live Demo

Here's a sample run choosing a unit from the database.

```text
╭──────────────────────────────────────────────╮
│        DEMON FARMING CALCULATOR (HotA)       │
╰──────────────────────────────────────────────╯
? Select option: Simple Calculator

? Select unit HP source: Select from database
? Select Faction: Bastion

╭───────────────────────────────────────────────────────────────────╮
│                        Select Unit (Bastion)                        │
├───────┬───────────────────┬────────┬───────┬──────────────────┬─────┤
│ Key   │ Non-Upgraded      │ HP     │ Key   │ Upgraded         │ HP  │
│ [1]   │ Centaur           │ 8      │ [11]  │ Kapitan Centaurów│ 10  │
│ ---   │ ---               │ ---    │ ---   │ ---              │ --- │
│ [2]   │ Leśny Elf         │ 15     │ [22]  │ Wielki Elf       │ 15  │
│ ---   │ ---               │ ---    │ ---   │ ---              │ --- │
│ [3]   │ Krasnolud         │ 20     │ [33]  │ Krasnoludzki Woj.│ 20  │
│ ---   │ ---               │ ---    │ ---   │ ---              │ --- │
│ [4]   │ Pegaz             │ 30     │ [44]  │ Srebrny Pegaz    │ 30  │
│ ---   │ ---               │ ---    │ ---   │ ---              │ --- │
│ [5]   │ Dendroid          │ 55     │ [55]  │ Dendroid Strażnik│ 65  │
│ ---   ...                 ...      ...     ...                ...   │
╰───────────────────────────────────────────────────────────────────╯
? Enter number (or '0' to cancel/back): 55
? Enter number of units (HP: 65): 10
? Enter number of Pit Lords (needed: 13): 5

╭────────────────────────────────────────────────────────────────╮
│                       Calculation Results                        │
│                                                                │
│    INPUT DATA                                                  │
│      ├─ Units:           10 x (HP: 65.0)                        │
│      ├─ Total HP Pool:   650                                    │
│      └─ Pit Lords Used:  5                                      │
│                                                                │
│    YIELD                                                       │
│      ├─ Max (from HP):   18.57                                  │
│      ├─ Max (from Lords): 7.14                                  │
│      └─ >>  ACTUALLY GAINED: 7.14 demons                        │
│                                                                │
│    OPTIMIZATION                                                │
│      ├─ Wasted HP:       20.00 (remainder)                      │
│      ├─ Needed Lords:    13 (for this stack)                    │
│      └─ Perfect Stack:   7 units (for 455 HP)                   │
│                                                                │
╰────────────────────────────────────────────────────────────────╯
╭──────────────────────────────────────────────────────────────────────────╮
│                         Local Distribution Chart                         │
│ [✓]    7 lords |   6 Units: [█         ]   11.14 Demons | Waste: 10.00 HP │
│ [✓]    8 lords |   7 Units: [█▍        ]   13.00 Demons | Waste:  0.00 HP |   <-- (PERFECT STACK)
│ [✓]   10 lords |   8 Units: [█▋        ]   14.86 Demons | Waste: 25.00 HP │
│ [✓]   11 lords |   9 Units: [█▊        ]   16.71 Demons | Waste: 15.00 HP │
│ [✓]   13 lords |  10 Units: [██        ]   18.57 Demons | Waste: 20.00 HP |   <-- (CURRENT) (Need +4 for PERFECTION)
│ [ ]   14 lords |  11 Units: [██▎       ]   20.43 Demons | Waste:  5.00 HP │
│ [ ]   16 lords |  12 Units: [██▌       ]   22.29 Demons | Waste: 30.00 HP │
│ [ ]   17 lords |  13 Units: [██▊       ]   24.14 Demons | Waste: 25.00 HP │
│ [ ]   19 lords |  14 Units: [███       ]   26.00 Demons | Waste:  0.00 HP |   <-- (PERFECT STACK)
╰──────────────────────────────────────────────────────────────────────────╯
╭────────────────────────────────────────────────────────────────────────╮
│                                  Legend                                │
│                                                                        │
│      [✓]/[ ] = Your 5 Pit Lords are enough for this stack                │
│      █       = *Potential* Demons from HP (scaled to list max)           │
│      Lords   = *Theoretical* Pit Lords needed for this stack             │
│                                                                        │
╰────────────────────────────────────────────────────────────────────────╯

... press Enter to calculate for another unit in this faction ...