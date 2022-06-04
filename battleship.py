from operator import ne


def validate_battlefield(field):
    # TEST 1: Total number of squares
    if sum([j for i in field for j in i]) != 20:
        return False
    # TEST 2: Count amount and length of straight lines
    considered = [[0 for i in range(10)] for _ in range(10)]
    distro = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    # TEST 2A: Find horizontal ships
    for r, row in enumerate(field):
        for c, cell in enumerate(row):
            
        
    for ship in distro:
        for r, row in enumerate(field):
            for c, cell in enumerate(row):
                if field[r][c] == 1:
                    pass
    # TEST 3A: Max # of 1's around another 1 = 1
    neighbors = []
    for r, row in enumerate(field):
        for c, _ in enumerate(row):
            ones = 0
            for x in range(max(0, c - 1), min(9, c + 1)):
                for y in range(max(0, r - 1), min(9, r + 1)):
                    if x != y:
                        if field[x][y] == 1:
                            ones += 1
            neighbors.append(ones)
    print(neighbors)
    # TEST 3B: No diagonal 1's

    return True


battleField = [
    [1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
    [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

print(validate_battlefield(battleField))
