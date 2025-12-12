# analysis.py
"""
Advanced Topics demo for Naasii project.

This script:
- uses numpy to simulate many Naasii starting rolls
- stores results in a pandas DataFrame
- uses seaborn/matplotlib to visualize how often
  pairs, triples, and runs appear
- uses time.process_time() to measure runtime
"""

import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def classify_roll(roll):
    """Given a list/array of 3 dice, return a label describing the pattern."""
    # work with 1–11 only; treat 12 as wild but here we just keep it as 12
    values = sorted(int(v) for v in roll)
    a, b, c = values

    # triple
    if a == b == c:
        return "three of a kind"

    # pair
    if a == b or b == c:
        # it is possible to also be part of a run, but we label as pair here
        return "pair"

    # run: strictly consecutive numbers
    if b == a + 1 and c == b + 1:
        return "run"

    return "no combo"


def simulate_starting_rolls(n_simulations=50_000, seed=None):
    """Simulate many Naasii starting rolls (3 white dice)."""
    if seed is not None:
        np.random.seed(seed)

    # each row is one roll, 3 columns for the 3 white dice
    rolls = np.random.randint(1, 13, size=(n_simulations, 3))
    categories = [classify_roll(row) for row in rolls]

    df = pd.DataFrame({
        "die1": rolls[:, 0],
        "die2": rolls[:, 1],
        "die3": rolls[:, 2],
        "pattern": categories,
    })
    return df


def main():
    print("Running Naasii starting roll analysis...")

    n_sim = 100_000

    start = time.process_time()
    df = simulate_starting_rolls(n_simulations=n_sim, seed=42)
    end = time.process_time()

    elapsed = end - start
    print(f"Simulated {n_sim} starting rolls in {elapsed:.4f} seconds.")

    # get counts and probabilities
    pattern_counts = df["pattern"].value_counts().reset_index()
    pattern_counts.columns = ["pattern", "count"]
    pattern_counts["probability"] = pattern_counts["count"] / n_sim

    print("\nEstimated probabilities for each pattern:")
    print(pattern_counts)

    # simple bar plot of probabilities
    plt.clf()
    sns.barplot(data=pattern_counts, x="pattern", y="probability")
    plt.title("Naasii: estimated probability of patterns on first roll")
    plt.ylabel("Probability")
    plt.xlabel("Pattern")
    plt.tight_layout()
    # plt.show()  # uncomment this line if running locally to see the plot

    # also save to file for reference
    plt.savefig("naasii_pattern_probabilities.png")
    print("\nSaved plot to naasii_pattern_probabilities.png")

    # example of reshaping data: count of each face value across all rolls
    value_counts = pd.Series(
        df[["die1", "die2", "die3"]].values.ravel()
    ).value_counts().reset_index()
    value_counts.columns = ["face", "count"]
    value_counts = value_counts.sort_values(by="face")

    plt.clf()
    sns.barplot(data=value_counts, x="face", y="count")
    plt.title("Frequency of each face value across all simulated dice")
    plt.xlabel("Die face (1–12)")
    plt.ylabel("Count")
    plt.tight_layout()
    # plt.show()  # uncomment to display
    plt.savefig("naasii_face_frequencies.png")
    print("Saved plot to naasii_face_frequencies.png")


if __name__ == "__main__":
    main()
