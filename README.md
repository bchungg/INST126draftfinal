
# Naasii: Simple Python Dice Game

## Overview

This project is a very basic version of Naasii: A Coyote & Crow Dice Game. I made it for a class assignment to practice Python, patterns, and some simple tool usage. It is not an official digital version of the real game, just a project.

## What the Game Does

The game lets two to five people play a simple version of Naasii. When the game starts, each player types in their name and chooses a lucky number from one to eleven. The number of rounds depends on how many people are playing. Two players get eleven rounds, three players get eight rounds, four players get six rounds, and five players get five rounds.

Each turn begins with three white dice. Players can roll up to four times. Before rolling again, they must lock at least one die so it stays in their hand. After the first roll, the game automatically adds two more white dice and one black die to follow the idea of how the real game works. Black dice have simple effects. A black twelve makes the player bust and score zero unless they have a white twelve that cancels it. Any other black value deletes all matching unlocked white dice. Deleted white dice get passed to the next player as extra starting dice.

At the end of the turn, the player chooses whether they want to score a set or a run. A set is three or more dice showing the same number. A run is three or more dice in order. White twelves are wild and can count as any number. Your score is how many dice are in the run.

Players also earn something called Nizi throughout the game. They get one Nizi whenever their lucky number appears on one of their rolls, three Nizi if they bust, and four Nizi if they do not score anything. At the end of the whole game, every three Nizi turn into one bonus point. After all rounds are complete, the program shows each player’s results,  Nizi totals, final score, and the winner.

## Simplifications

It does not include the optional Nizi abilities from the actual physical game. It does not track the printed score sheet, so players can score the same type as many times as they want. It also does not limit the number of dice in the box. Instead, any deleted white die simply becomes an extra die for the next player. White twelves are always used automatically to block black twelves without asking the player.


## How to Run

You just need Python 3 to run the game. 


