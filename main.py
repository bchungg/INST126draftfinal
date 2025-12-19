import random


def roll_dice(num_dice):
    """Roll num_dice 12-sided dice and return a list of numbers."""
    dice = []
    for i in range(num_dice):
        value = random.randint(1, 12)
        dice.append(value)
    return dice


def get_int(prompt, min_value, max_value):
    while True:
        num = input(prompt)

        # check if it's a number
        if not num.isdigit():
            print("Please enter a number.")
            continue

        num = int(num)

        # check if it's in range
        if min_value <= num <= max_value:
            return num
        else:
            print("Please enter a number between", min_value, "and", max_value)


def score_set(dice):
    """Score a set: choose a number and count how many dice show that number."""
    print("Your dice:", dice)
    choice = get_int("What number do you want to score a set of (1-12)? ", 1, 12)

    count = 0
    for value in dice:
        if value == choice:
            count += 1

    if count < 3:
        print("You need at least 3 of the same number. No score this turn.")
        return 0
    else:
        print("You scored a set of", choice, "with", count, "dice. Points:", count)
        return count


def longest_run_length(dice):
    """Find the longest run of consecutive numbers in the dice."""
    if len(dice) == 0:
        return 0

    sorted_dice = sorted(dice)
    best = 1
    current = 1

    for i in range(1, len(sorted_dice)):
        if sorted_dice[i] == sorted_dice[i - 1] + 1:
            current += 1
            if current > best:
                best = current
        elif sorted_dice[i] == sorted_dice[i - 1]:
            # same number, ignore
            continue
        else:
            current = 1

    return best


def score_run(dice):
    """Score a run: longest streak of consecutive numbers is the score."""
    print("Your dice:", dice)
    length = longest_run_length(dice)

    if length < 3:
        print("You need a run of at least 3 numbers.")
        return 0
    else:
        print("You scored a run of length", length, "points:", length)
        return length


def take_turn(player_name, round_number):
    """One turn for a single player."""
    print("\n=== Round", round_number, "-", player_name, "===")

    num_dice = 3
    dice = []
    roll = 1

    while roll <= 4:
        input("Press Enter to roll (roll " + str(roll) + " of 4)...")
        dice = roll_dice(num_dice)
        print("You rolled:", dice)

        if roll == 4:
            print("This was your 4th roll. You have to score now.")
            break

        choice = input("Type 'r' to roll again or 's' to stop and score: ").strip().lower()
        while choice not in ["r", "s"]:
            choice = input("Please type 'r' (roll) or 's' (score): ").strip().lower()

        if choice == "s":
            break
        else:
            roll += 1

    print("\nTime to score!")
    print("Your final dice:", dice)

    kind = input("Type 's' to score a set or 'r' to score a run: ").strip().lower()
    while kind not in ["s", "r"]:
        kind = input("Please type 's' for set or 'r' for run: ").strip().lower()

    if kind == "s":
        return score_set(dice)
    else:
        return score_run(dice)


def main():
    print("Welcome to Naasii")
    print("This is a dice game for 2–5 players.\n")

    num_players = get_int("How many players (2-5)? ", 2, 5)

    players = []
    for i in range(num_players):
        name = input("Enter name for Player " + str(i + 1) + ": ").strip()
        if name == "":
            name = "Player " + str(i + 1)
        players.append(name)

    if num_players in [2, 3]:
        total_rounds = 5
    else:
        total_rounds = 4

    print("\nThe game will be", total_rounds, "rounds.\n")

    scores = [0] * num_players

    for r in range(1, total_rounds + 1):
        for i in range(num_players):
            points = take_turn(players[i], r)
            scores[i] += points
            print(players[i], "scored", points, "this round. Total:", scores[i])

    print("\n=== Final Scores ===")
    best_score = None
    winner = None

    for i in range(num_players):
        print(players[i] + ":", scores[i], "points")
        if best_score is None or scores[i] > best_score:
            best_score = scores[i]
            winner = players[i]

    print("\nWinner:", winner, "with", best_score, "points!")


if __name__ == "__main__":
    main()