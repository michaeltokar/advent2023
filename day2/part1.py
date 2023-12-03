import sys

# The Elf would first like to know which games would have been possible if the bag
# contained only 12 red cubes, 13 green cubes, and 14 blue cubes?

limits = {
    'red': 12,
    'green': 13,
    'blue': 14
}

def parse_set(set_str):
    cubes = set_str.strip().split(',')
    result = {
        'red': 0,
        'green': 0,
        'blue': 0
    }
    for cube in cubes:
        elements = cube.strip().split(' ')
        result[elements[1]] = int(elements[0])
    return result

def parse_game(line):
    elements = line.strip().split(':')
    result = {
        'id': int(elements[0][5:]),
        'sets': [parse_set(s) for s in elements[1].split(';')]
    }
    return result

# Test if a game exceeds the limits
def game_match(game):
    for s in game['sets']:
        if s['red'] > limits['red'] or s['green'] > limits['green'] or s['blue'] > limits['blue']:
            return 0
    return 1

# Read input lines until EOF (Ctrl+D)
score = 0
for line in sys.stdin:
    game = parse_game(line)
    print(game)
    score += game_match(game) * game['id']
    
print(score)
