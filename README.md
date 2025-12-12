<<<<<<< HEAD
# Naasii: A Coyote & Crow Dice Game (Python Project)

## Overview

This repository contains an **unofficial, text-based Python implementation** of  
**Naasii: A Coyote & Crow Dice Game**, plus a small data analysis script that
uses `numpy`, `pandas`, `matplotlib`, and `seaborn` to study dice rolls.

The code was written as a class project to practice Python programming,
patterns, and tools. It is not an official digital version of the game.

---

## What the Program Does

### `main.py` — Play the Game

- Supports **2–5 players**.
- Asks each player for:
  - their **name**
  - their **Lucky Number** (1–11).
- Sets the number of rounds based on the player count:
  - 2 players → 11 rounds  
  - 3 players → 8 rounds  
  - 4 players → 6 rounds  
  - 5 players → 5 rounds  

On each player’s turn:

- Starts by rolling **3 white (Coyote) dice**.
- The player must **lock at least 1 die** before rolling again.
- The player may roll up to **4 times total**.
- After the first roll, later rolls:
  - add **2 more white dice** and **1 black (Crow) die** to the pool,
    similar to the tabletop rules.
- **Black dice**:
  - A black **12** causes a **bust** (score 0 for the round),
    **unless** there is a white 12 available.
  - The program automatically **eliminates white 12s** to cancel black 12s
    whenever possible.
  - Any non-12 black value **eliminates** all matching **unlocked white dice**.
    Those eliminated dice are “passed” to the next player, who starts their
    next turn with extra white dice.
- **White 12s** are treated as **wild** and can count as any value 1–11
  when scoring.

Scoring:

- At the end of the turn, the player can score either:
  - a **Set** (3 or more of the same number), or
  - a **Run** (3 or more numbers in a row).
- The program asks:
  - whether they want to score a **set** or **run**, and
  - which number (for a set) or **starting number** (for a run).
- Wild 12s are used automatically to help complete the chosen set or run.
- The number of dice used in the set or run becomes the **points** for that round.

Nizi:

- Players gain **Nizi** during the game:
  - **+1 Nizi** whenever a player’s Lucky Number appears on their own roll.
  - **+3 Nizi** for a **Bust**.
  - **+4 Nizi** for **No Score** (when they cannot form any valid set or run,
    or they choose an invalid score).
- At the end of the game, every **3 Nizi = +1 bonus point** added to the
  player’s total score.

Game end:

- After all rounds, the program:
  - shows each player’s round scores,
  - shows total Nizi and Nizi bonus,
  - computes each player’s **final score**,
  - announces the winner (or a tie).

---

## Simplifications and Limitations

To keep the code manageable for a class project, this version simplifies
some parts of the physical game:

- **Optional Nizi abilities** (Adjust, Re-roll, Flip, Pair, Small, Twelve,
  Repeat, Evade, Wild) are **not implemented**.
- The program does not track the exact limited number of **Run** and **Set**
  boxes from the printed score sheet. Players can conceptually score the same
  type more than once.
- The handling of eliminated white dice is modeled as:
  - every eliminated die simply gives the **next player** one extra white die
    on their next turn. The program does not enforce the physical limit of
    exactly 9 white dice in the box.
- White 12s used to cancel black 12s are always sacrificed **automatically**
  to avoid a bust whenever possible.

These details are explained so that the behavior of the program matches
what is described here, even if it is not a perfect simulation of the
tabletop rules.

---

## `analysis.py` — Advanced Topics Script

The file `analysis.py` is a small data analysis script that demonstrates
the use of the following Python modules:

- `time`
- `numpy`
- `pandas`
- `matplotlib`
- `seaborn`

What it does:

- Simulates **many Naasii starting rolls** (3 white dice each) using `numpy`.
- Classifies each roll as:
  - “no combo”
  - “pair”
  - “three of a kind”
  - “run”
- Stores the results in a `pandas` DataFrame.
- Uses `time.process_time()` to measure how long the simulation takes.
- Calculates and prints the estimated probability of each pattern.
- Uses `seaborn` and `matplotlib` to create:
  - a bar plot of pattern probabilities, saved as
    `naasii_pattern_probabilities.png`.
  - a bar plot of the overall frequency of each face value (1–12), saved as
    `naasii_face_frequencies.png`.

This script is separate from the main game, but it is related to Naasii
and is meant to demonstrate “Advanced Topics” tools for the course.

---

## How to Run the Program

Requirements:

- Python 3
- For `analysis.py`, you also need:
  - `numpy`
  - `pandas`
  - `matplotlib`
  - `seaborn`

You can install these with:

```bash
pip install numpy pandas matplotlib seaborn
=======
# Naasii-INST126Final-
This project is a Python version of the Naasii dice game. Players roll, score, and compete using turn-based gameplay. A separate script simulates 100k rolls using numpy and pandas to analyze probabilities and creates visual charts with matplotlib and seaborn.
>>>>>>> df100e5f3961419c977435527bd2629fb9b33c3e
