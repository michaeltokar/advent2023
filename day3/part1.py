import sys
import re

max_dim = 140
number_state = []
symbol_state = [[0] * max_dim for _ in range(max_dim)]
npat = r'\d'
# RE pattern for symbols
spat = r'[^0-9. ]'

def add_symbol_state(c, x, y):
    print(c, x, y)
    symbol_state[x][y] = 1

def add_number_state(row, npos, nbuffer):
    result = {
        'num': int(nbuffer),
        'len': len(nbuffer),
        'y': npos,
        'x': row
    }
    number_state.append(result)

# Parse a line
def parse_line(line, x):
    #print(row, line)
    
    nbuffer = None
    npos = None
    y = 0
    # read each character in the line
    for c in line:
        if re.match(npat, c):
            # digit found - possibly new number or existing
            if nbuffer is None:
                # initialise buffer
                npos = y
                nbuffer = c
            else:
                nbuffer += c
        else:
            if not nbuffer is None:
                # number is finished, flush buffer
                add_number_state(x, npos, nbuffer)
                nbuffer = None
                npos = None
            if re.match(spat, c):
                # found a symbol
                add_symbol_state(c, x, y)

        y += 1

    # check if number was at end of line
    if not nbuffer is None:
        # number is finished, flush buffer
        add_number_state(x, npos, nbuffer)

# Check a found number to see if it is adjacent to symbols
def is_number_adjacent(number):
    x = number['x']
    y = number['y']
    num = number['num']
    print(f"Testing {num} at ({x},{y})")
    for i in range(x-1, x+2, 1):
        for j in range(y-1, y+number['len']+1, 1):
            if i < 0 or i >= max_dim:
                continue
            if j < 0 or j >= max_dim:
                continue
            if symbol_state[i][j] > 0:
                print(f"{num} is a match")
                return num

    return 0

# Read input lines until EOF (Ctrl+D)
row = 0
for line in sys.stdin:
    parse_line(line.strip(), row)
    row += 1

score = 0
for n in number_state:
    score += is_number_adjacent(n)
    
print(number_state)
print(symbol_state)
print(score)
