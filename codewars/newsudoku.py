
def pre_solve(grid):
    change = True
    while change:
        change = False
        for y,line in enumerate(grid):
            for x, _ in enumerate(line):
                if grid[x][y] == 0:
                    options = search_unique(grid, x,y)
                    if len(options) == 1:
                        grid[x][y] = options[0]
                        change = True
    return grid


def search_unique(grid, x,y):
    # Test 1: Vertical and horizontal unique number

    # Test 2: Last number in quadrant

    # Test 3: Last number in line (vertical or horizontal)

