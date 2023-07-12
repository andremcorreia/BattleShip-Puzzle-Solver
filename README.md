# Bimaru / Yubotu / Battleship Puzzle Solver

This project was part of the Artificial Intelligence (AI) course and aims to develop a Python program that solves the Bimaru problem using AI techniques. 
Bimaru, also known as Battleship Puzzle, Yubotu, or Solitaire Battleship, is a puzzle inspired by the well-known game Battleship between two players.


## Implementation

Bimaru.py: The main program capable of solving Bimaru puzzles. Use the following command to run the program:
  - python3 bimaru.py < <instance_file> 
  - Use python or py instead of python3 depending on your system configuration.

autotester.py: A script that attempts to find a puzzle that the Bimaru solver (bimaru.py) cannot solve indefinitely.

Tests/: Folder with manual test cases.

## Input Format

The input format for the Bimaru puzzles should follow this structure:

```
ROW <count-0> ... <count-9>
COLUMN <count-0> ... <count-9>
<hint total>
HINT <row> <column> <hint value>
```

## Example Output Format

The solved puzzle will be displayed in the following format:

```
c...lr....
..tW......
..b.......
......lmr.
c.t.......
..m....c..
tWb...W...
b.........
.....lmmr.
c.....W...
```

Capital letters correspond to the hints given, with "." and "W" representing water cells.
The letters "t", "b", "l", "r", "m", and "c" represent the ship orientation: top, bottom, left, right, middle, or single ship, respectively.

