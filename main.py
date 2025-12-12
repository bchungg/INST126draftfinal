# main.py
"""
Naasii: A Coyote & Crow Dice Game (unofficial text-based version)

This is a simple console implementation for 2–5 players.
It follows the core rules:
- runs and sets
- up to 4 rolls per turn
- black crow die can bust you or eliminate white dice
- lucky numbers
- Nizi from busts, no score, and lucky numbers
"""

import random

#helper functions 

def roll_dice(num, sides=12):
    """Roll `num` dice with `sides` sides and return a list of ints."""
    return [random.randint(1, sides) for _ in range(num)]


def display_dice(label, dice):
    """Pretty-print a list of dice values."""
    if not dice:
        print(f"{label}: (none)")
    else:
        print(f"{label}: " + " ".join(str(v) for v in dice))


def choose_int(prompt, valid_range):
    """Ask user for an integer inside valid_range (inclusive)."""
    while True:
        try:
            value = int(input(prompt))
            if value in valid_range:
                return value
            print(f"Please enter a number in {valid_range.start}–{valid_range.stop - 1}.")
        except ValueError:
            print("Please enter a whole number.")


def choose_indices_to_lock(unlocked):
    """Ask the player which dice to lock from unlocked list.
    Returns list of indices (0-based) to lock.
    """
    if not unlocked:
        return []
    while True:
        print("Unlocked dice (index:value):")
        for i, val in enumerate(unlocked, start=1):
            print(f"  {i}: {val}")
        raw = input("Enter indexes of dice to lock (space-separated, at least one): ").strip()
        parts = raw.split()
        if not parts:
            print("You must lock at least one die.")
            continue
        try:
            idxs = sorted({int(p) - 1 for p in parts})
        except ValueError:
            print("Please enter only numbers.")
            continue
        if any(i < 0 or i >= len(unlocked) for i in idxs):
            print("One of those indexes is out of range.")
            continue
        return idxs


def can_score_set(all_dice, target):
    """Return how many dice can be used in a Set of `target` (1–11) using wild 12s.
    If fewer than 3, return 0.
    """
    if target < 1 or target > 11:
        return 0
    normal = sum(1 for v in all_dice if v == target)
    wilds = sum(1 for v in all_dice if v == 12)
    total = normal + wilds
    return total if total >= 3 else 0


def run_length_with_start(all_dice, start):
    """Return length of a run starting at `start` (1–11) using wild 12s.
    If length < 3, return 0.
    """
    if start < 1 or start > 11:
        return 0
    counts = {n: 0 for n in range(1, 12)}
    wilds = 0
    for v in all_dice:
        if v == 12:
            wilds += 1
        elif 1 <= v <= 11:
            counts[v] += 1
    used = 0
    current = start
    while current <= 11:
        if counts[current] > 0:
            counts[current] -= 1
            used += 1
        elif wilds > 0:
            wilds -= 1
            used += 1
        else:
            break
        current += 1
    return used if used >= 3 else 0


#core turn logic 

def take_turn(player, round_index, extra_starting_white):
    """
    Handle a single player's turn.
    Returns (round_score, nizi_gain, extra_white_for_next_player).
    """
    name = player["name"]
    lucky_number = player["lucky"]

    locked_white = []
    unlocked_white = 3 + extra_starting_white
    unlocked_black = 0

    extra_white_for_next = 0
    total_nizi_gain = 0

    print(f"\n=== Round {round_index + 1} — {name}'s turn ===")
    print(f"Starting with {unlocked_white} white dice.")

    bust = False

    for roll_num in range(1, 5):
        #build lists of actual dice values
        white_rolls = roll_dice(unlocked_white) if unlocked_white > 0 else []
        black_rolls = roll_dice(unlocked_black) if unlocked_black > 0 else []

        print(f"\nRoll {roll_num}:")
        display_dice("Locked white", locked_white)
        display_dice("Rolled white", white_rolls)
        display_dice("Rolled black", black_rolls)

        #lucky number triggers on any white dice this roll
        lucky_hits = sum(1 for v in white_rolls if v == lucky_number)
        if lucky_hits > 0:
            print(f"{name}'s lucky number {lucky_number} rolled {lucky_hits} time(s)! +{lucky_hits} Nizi.")
            total_nizi_gain += lucky_hits

        #handle black dice: bust or elimination
        #first use white 12s automatically to block black 12s if possible
        total_white_12 = (
            sum(1 for v in locked_white if v == 12)
            + sum(1 for v in white_rolls if v == 12)
        )
        num_black_12 = sum(1 for v in black_rolls if v == 12)

        #each white 12 can cancel one black 12 by being eliminated
        black_12s_causing_bust = max(0, num_black_12 - total_white_12)
        white_12s_to_eliminate = min(num_black_12, total_white_12)

        if white_12s_to_eliminate > 0:
            print(f"Auto-avoiding bust by eliminating {white_12s_to_eliminate} white 12(s).")
            #eliminate from unlocked first, then locked
            for _ in range(white_12s_to_eliminate):
                if 12 in white_rolls:
                    white_rolls.remove(12)
                elif 12 in locked_white:
                    locked_white.remove(12)
                extra_white_for_next += 1  #eliminated die passed to next player

        if black_12s_causing_bust > 0:
            print("Black 12 rolled and no white 12 left to save you. BUST!")
            bust = True
            break

        #handle non-12 black dice: eliminate matching unlocked white dice
        for b in black_rolls:
            if b == 12:
                continue
            eliminated_here = [v for v in white_rolls if v == b]
            if eliminated_here:
                print(f"Black die {b} eliminates white dice: {eliminated_here}")
                count = len(eliminated_here)
                extra_white_for_next += count
                white_rolls = [v for v in white_rolls if v != b]

        #update unlocked whites list with what remains from this roll
        #(they are all currently unlocked)
        unlocked_values = white_rolls

        #if no dice at all available (locked + unlocked), you bust
        if not locked_white and not unlocked_values:
            print("No dice available to lock — automatic BUST.")
            bust = True
            break

        #decide whether to stop or roll again
        all_current_dice = locked_white + unlocked_values
        display_dice("All dice in play", all_current_dice)

        if roll_num == 4:
            print("You have used all 4 rolls; you must score now.")
            locked_white.extend(unlocked_values)
            unlocked_white = 0
            break

        #ask player: score or roll again
        choice = input("Type 's' to score now, or 'r' to roll again: ").strip().lower()
        while choice not in ("s", "r"):
            choice = input("Please type 's' (score) or 'r' (roll again): ").strip().lower()

        if choice == "s":
            locked_white.extend(unlocked_values)
            unlocked_white = 0
            break

        #player wants to roll again: must lock at least one die from unlocked
        if not unlocked_values:
            print("No unlocked dice to lock — you cannot roll again, so you must score.")
            locked_white.extend(unlocked_values)
            unlocked_white = 0
            break

        idxs = choose_indices_to_lock(unlocked_values)
        # move those dice to locked
        new_locked = [unlocked_values[i] for i in idxs]
        for i in reversed(idxs):
            unlocked_values.pop(i)
        locked_white.extend(new_locked)

        print(f"Locked dice now: {locked_white}")
        # set counts for next roll
        unlocked_white = len(unlocked_values) + 2  # pick up unlocked + add 2 white
        unlocked_black = len(black_rolls) + 1      # pick up black + add 1 more

    #scoring / bust / no score
    if bust:
        print(f"{name} busted this round. Score = 0, +3 Nizi.")
        total_nizi_gain += 3
        return 0, total_nizi_gain, extra_white_for_next

    all_dice = locked_white
    print("\nEnd of turn dice:")
    display_dice("All dice used for scoring", all_dice)

    if len(all_dice) < 3:
        print("Fewer than 3 dice — cannot score. No Score: 0 points, +4 Nizi.")
        total_nizi_gain += 4
        return 0, total_nizi_gain, extra_white_for_next

    # ask player whether to score a set or run
    kind = input("Score a (s)et or a (r)un? ").strip().lower()
    while kind not in ("s", "r"):
        kind = input("Please type 's' for set or 'r' for run: ").strip().lower()

    score = 0
    if kind == "s":
        target = choose_int("Which number are you scoring a set of (1–11)? ", range(1, 12))
        used = can_score_set(all_dice, target)
        if used == 0:
            print("You cannot make a valid set with that number. This counts as No Score (0 points, +4 Nizi).")
            total_nizi_gain += 4
            score = 0
        else:
            score = used
            print(f"Scored a set of {target}s using {used} dice. +{score} points.")

    else:  #run
        start = choose_int("What is the starting number of your run (1–11)? ", range(1, 12))
        length = run_length_with_start(all_dice, start)
        if length == 0:
            print("You cannot make a valid run with that starting number. This counts as No Score (0 points, +4 Nizi).")
            total_nizi_gain += 4
            score = 0
        else:
            print(f"Scored a run starting at {start} of length {length}. +{length} points.")
            score = length

    return score, total_nizi_gain, extra_white_for_next


#main game loop

def rounds_for_player_count(n_players):
    """Return number of rounds based on number of players."""
    mapping = {
        2: 11,
        3: 8,
        4: 6,
        5: 5,
    }
    return mapping.get(n_players, 11)


def main():
    print("Welcome to Naasii: A Coyote & Crow Dice Game (unofficial text version)")
    print("This program is for 2–5 players sharing one screen.\n")

    n_players = choose_int("How many players (2–5)? ", range(2, 6))

    players = []
    for i in range(n_players):
        name = input(f"Enter name for Player {i + 1}: ").strip() or f"Player {i + 1}"
        lucky = choose_int(f"{name}, choose your Lucky Number (1–11): ", range(1, 12))
        players.append({
            "name": name,
            "lucky": lucky,
            "scores": [],
            "nizi": 0,
        })

    total_rounds = rounds_for_player_count(n_players)
    print(f"\nGame will be {total_rounds} rounds.")

    #extra white dice passed to next player from eliminations
    extra_white_for_player = [0] * n_players

    for r in range(total_rounds):
        for p_index, player in enumerate(players):
            extra_starting = extra_white_for_player[p_index]
            extra_white_for_player[p_index] = 0  # will be consumed now

            score, nizi_gain, extra_for_next = take_turn(player, r, extra_starting)
            player["scores"].append(score)
            player["nizi"] += nizi_gain

            #pass eliminated dice to next player
            next_index = (p_index + 1) % n_players
            extra_white_for_player[next_index] += extra_for_next

            print(f"{player['name']} ends the round with +{score} points and +{nizi_gain} Nizi (total Nizi = {player['nizi']}).")

    #end game scoring
    print("\n=== Final Scoring ===")
    best_score = None
    winners = []

    for player in players:
        total_round_points = sum(player["scores"])
        bonus_from_nizi = player["nizi"] // 3
        final_score = total_round_points + bonus_from_nizi
        print(f"\nPlayer: {player['name']}")
        print(f"  Round scores: {player['scores']}")
        print(f"  Nizi: {player['nizi']} (bonus {bonus_from_nizi} points)")
        print(f"  FINAL SCORE: {final_score}")

        if best_score is None or final_score > best_score:
            best_score = final_score
            winners = [player["name"]]
        elif final_score == best_score:
            winners.append(player["name"])

    if len(winners) == 1:
        print(f"\nWinner: {winners[0]} with {best_score} points!")
    else:
        print(f"\nTie! Winners: {', '.join(winners)} with {best_score} points.")


if __name__ == "__main__":
    main()
