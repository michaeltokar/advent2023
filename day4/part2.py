import sys
import re

max_dim = 214
card_wins = [ 0 for _ in range(0, max_dim+1) ]
card_pile = [ 1 for _ in range(0, max_dim+1) ]
card_pile[0] = 0

# Convert an array of strings to an array of numbers
def to_number_set(arr):
    return set([ int(x) for x in arr ])

# Figure out the score for a single card
def parse_card(line):
    parts = re.split(r'[:\|]', line)

    card = int(parts[0][5:])
    wins = to_number_set(re.split(r'\s+', parts[1].strip()))
    picks = to_number_set(re.split(r'\s+', parts[2].strip()))

    print(f"Card: {card}")
    print(f"Wins: {wins}")
    print(f"Picks: {picks}")
    score = 0
    for w in wins:
        if w in picks:
            score += 1

    print(f"Score: {score}")
    card_wins[card] = score
    return {'card': card, 'score': score}


# Read input lines until EOF (Ctrl+D)
for line in sys.stdin:
    parse_card(line.strip())

# Now go through all results and 'copy' the cards
# i = each card played
for i in range(1, max_dim):
    # j = how many of that card there are: e.g. if card_pile[3] = 2 then you apply the wins of card 3 twice
    for j in range(card_pile[i]):
        # how many winning numbers were on card i => how many subsequent cards get copied
        wins = card_wins[i]
        # k = the subsequent cards that get copied. Note: don't copy the current card.
        for k in range(wins, 0, -1):
            card_pile[i+k] += 1
    
# final score is how many cards (incl. copies) we ended up with
score = sum(card_pile)

print(card_wins)
print(card_pile)
print(f"Final score: {score}")
