import sys

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

# Calculate the game power: maximum of red, green, blue seen multiplied together
# e.g. if max red was 6; max green was 2; max blue was 4; then power = 6 * 2 * 4 = 48
def game_power(game):
    power = {
        'red': 0,
        'green': 0,
        'blue': 0
    }
    for s in game['sets']:
        if s['red'] > power['red']:
            power['red'] = s['red']
        if s['green'] > power['green']:
            power['green'] = s['green']
        if s['blue'] > power['blue']:
            power['blue'] = s['blue']
    return power['red'] * power['green'] * power['blue']

# Read input lines until EOF (Ctrl+D)
score = 0
for line in sys.stdin:
    game = parse_game(line)
    print(game)
    score += game_power(game)
    
print(score)
