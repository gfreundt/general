import random
import csv
import os
import time
import sys

sys.setrecursionlimit = 10000000


def print_maze(maze):
    os.system("cls")
    for row in maze:
        line = []
        for c in row:
            if c == 1:
                symbol = "█"
            elif c in (2, 3):
                symbol = "O"
            elif c == ".":
                symbol = "."
            else:
                symbol = " "
            line.append(symbol)
        print("".join(line))


def creator(height, width, saturation):
    array = [[1] * width]
    for _ in range(height - 2):
        line = [1]
        for _ in range(width - 2):
            pixel = 1 if random.randint(1, 100) <= saturation else 0
            line.append(pixel)
        line.append(1)
        array.append(line)
    array.append([1] * width)

    array[0][1] = 2
    array[height - 1][width - 2] = 3

    print_maze(array)

    with open("maze.csv", "w", newline="", encoding="utf-8") as outfile:
        csv.writer(outfile).writerows(array)

    return array


def get_possible_destinations(maze, pos, been_there):
    moves = []
    for hops in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        coords = (pos[0] + hops[0], pos[1] + hops[1])
        # print(pos, coords)
        pixel = maze[coords[0]][coords[1]]
        if pixel == 0 and pixel not in been_there:
            moves.append(coords)
        if pixel == 3:
            print("Success!")
            print(time.time() - start)
            print_maze(maze)
            exit()
    return moves


def solve_maze(maze, pos, path, been_there):

    if maze[pos[0]][pos[1]] == 3:
        print("Solved!")
        exit()
    # print_maze(maze)
    # print(time.time())
    # time.sleep(0.01)
    destinations = get_possible_destinations(maze, pos, been_there)
    for dest in destinations:
        path.append(dest)
        maze[dest[0]][dest[1]] = "."
        solve_maze(maze, pos=dest, path=path, been_there=been_there)


def load_maze(filename="maze.csv"):
    with open(filename, "r") as file:
        return [[int(i) for i in j] for j in csv.reader(file)]


maze = load_maze("maze1.csv")
print_maze(maze)
maze = creator(50, 60, 30)

start = time.time()
solve_maze(maze, pos=(0, 1), path=[], been_there=[])
print("NO PATH")
