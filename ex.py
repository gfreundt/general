def valid_moves(pos, maze, N):
    x, y = pos[0], pos[1]
    moves = ""
    # north
    if y > 0 and maze[y - 1][x] != "W":
        moves += "N"
    # south
    if y < N - 1 and maze[y + 1][x] != "W":
        moves += "S"
    # west
    if x > 0 and maze[y][x - 1] != "W":
        moves += "W"
    # east
    if x < N - 1 and maze[y][x + 1] != "W":
        moves += "E"
    return moves


def move(pos, maze, N, tm, depth):
    if depth > 8:
        return
    print(f"{pos=}, {tm=}")
    if pos == [N - 1, N - 1]:
        print("True")
        quit()
    print("vms:", valid_moves(pos, maze, N))
    for mv in valid_moves(pos, maze, N):
        print(f"{mv=} {depth=}")
        if mv == "N" and tm[-1] != "S":
            pos[1] -= 1
            tm += mv
            move(pos, maze, N, tm, depth + 1)
        elif mv == "S" and tm[-1] != "N":
            print("in")
            pos[1] += 1
            tm += mv
            move(pos, maze, N, tm, depth + 1)
        elif mv == "W" and tm[-1] != "E":
            pos[0] -= 1
            tm += mv
            move(pos, maze, N, tm, depth + 1)
        elif mv == "E" and tm[-1] != "W":
            pos[0] += 1
            tm += mv
            move(pos, maze, N, tm, depth + 1)
    tm = tm[:-1]


def path_finder(maze):
    # setup
    maze = maze.replace("\n", "")
    N = int(len(maze) ** 0.5)
    maze = [maze[i * N : (i + 1) * N] for i in range(N)]
    pos = [0, 0]
    # finder
    move(pos, maze, N, "@", 0)


a = "\n".join([".W...", ".W...", ".W.W.", "...W.", "...W."])
print(path_finder(a))
