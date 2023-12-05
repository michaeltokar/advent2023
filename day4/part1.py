import sys
import re

# Convert an array of strings to an array of numbers
def to_number_set(arr):
    return set([ int(x) for x in arr ])

# Figure out the score for a single game (row)
def parse_game(line):
    parts = re.split(r'[:\|]', line)
    wins = to_number_set(re.split(r'\s+', parts[1].strip()))
    picks = to_number_set(re.split(r'\s+', parts[2].strip()))

    print(f"Wins: {wins}")
    print(f"Picks: {picks}")
    score = 0
    for w in wins:
        if w in picks:
            if score == 0:
                score = 1
            else:
                score *= 2

    print(f"Score: {score}")
    return score


# Read input lines until EOF (Ctrl+D)
score = 0
for line in sys.stdin:
    score += parse_game(line.strip())
    

print(f"Final score: {score}")
