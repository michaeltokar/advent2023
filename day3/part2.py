import sys
import re

# Note: unlike Part 1, Part 2 assumes 'symbol' is only '*'

class ANumber:
    def __init__(self, num, length, x, y):
        self.num = num
        self.length = length
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, ANumber):
            return (self.num, self.x, self.y) == (other.num, other.x, other.y)
        return False

    def __hash__(self):
        # Ensure instances of ANumber are hashable
        return hash((self.num, self.x, self.y))

    def __str__(self):
        return f"{self.num} @ ({self.x},{self.y})"

max_dim = 140
number_state = []
symbol_state = []
number_map = [[0] * max_dim for _ in range(max_dim)]
#symbol_map = [[0] * max_dim for _ in range(max_dim)]
npat = r'\d'
# RE pattern for symbols
spat = r'\*'

# Record the symbol in the list of seen symbols, with its x,y coords
def add_symbol_state(c, x, y):
    print(c, x, y)
    #symbol_map[x][y] = 1
    symbol_state.append({'x': x, 'y': y})

def add_number_state(x, y, nbuffer):
    result = ANumber(int(nbuffer), len(nbuffer), row, y)
    print(f"Adding {result} to number state")
    # Add number and its details to list of seen numbers
    number_state.append(result)

    # Also flag this number in the number map for each coordinate it appears on
    for j in range(y, y+result.length, 1):
        # print(f"Adding {result} to ({x},{j})")
        number_map[x][j] = result


# Parse a line
def parse_line(line, x):
    #print(row, line)
    
    # Current number buffer
    nbuffer = None
    # Which coordinate the current number in buffer started on
    npos = None
    # Which coordinate does current character appear at
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

# Check if a found symbol is adjacent to two* numbers, thus making it a gear
# If so, return the multiplication of the numbers
def is_symbol_adjacent(symbol):
    x = symbol['x']
    y = symbol['y']
    print(f"Testing symbol at ({x},{y})")

    # Store all the found numbers
    # Note we are not strictly looking for two numbers here
    # Using a set because the found numbers appear in each
    # coordinate in the number map, so we do not want to
    # duplicate the numbers
    nfound = set()

    for i in range(x-1, x+2, 1):
        for j in range(y-1, y+2, 1):
            if i < 0 or i >= max_dim:
                continue
            if j < 0 or j >= max_dim:
                continue
            n = number_map[i][j]
            print(f"({i},{j}) = {n}")
            if isinstance(n, ANumber):
                nfound.add(n)

    print(f"All found numbers for this symbol: {nfound}")
    if len(nfound) <= 1:
        return 0
    
    result = 1
    for n in nfound:
        result *= n.num
    return result

# Read input lines until EOF (Ctrl+D)
row = 0
for line in sys.stdin:
    parse_line(line.strip(), row)
    row += 1

score = 0
for s in symbol_state:
    score += is_symbol_adjacent(s)
    
print(number_state)
# print(number_map)
print(symbol_state)
print(score)
