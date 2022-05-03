from mazes import creator, print_maze
import os, time
import pygame

pygame.init()


def draw_maze(maze):

    scale = 25
    xmargin, ymargin = 40, 20

    TOP_LEFT = (xmargin, ymargin)
    TOP_RIGHT = ((len(maze) - 1) * scale + xmargin, ymargin)
    BOT_LEFT = (xmargin, (len(maze[0]) - 1) * scale + ymargin)
    BOT_RIGHT = (
        (len(maze) - 1) * scale + xmargin,
        (len(maze[0]) - 1) * scale + ymargin,
    )

    print(f"{TOP_LEFT=} {TOP_RIGHT=} {BOT_LEFT=} {BOT_RIGHT=}")

    pygame.draw.line(screen, WHITE, TOP_LEFT, TOP_RIGHT)
    pygame.draw.line(screen, WHITE, TOP_RIGHT, BOT_RIGHT)
    pygame.draw.line(screen, WHITE, BOT_RIGHT, BOT_LEFT)
    pygame.draw.line(screen, WHITE, BOT_LEFT, TOP_LEFT)

    """
    for r, row in enumerate(maze[1:-1]):
        for c, cell in enumerate(row[1:-1]):

            if maze[r + 1][c] == 1:
                pygame.draw.line(
                    screen,
                    WHITE,
                    (r * scale + xmargin, c * scale + ymargin),
                    (r * scale + xmargin, (c + 1) * scale + ymargin),
                )

            if maze[r][c + 1] == 1:
                pygame.draw.line(
                    screen,
                    WHITE,
                    (r * scale + xmargin, c * scale + ymargin),
                    ((r + 1) * scale + xmargin, c * scale + ymargin),
                )
    """

    for row in range(len(maze)):
        for col in range(len(maze[0])):
            print(row, col)
            if maze[row][col] == 1:
                x0 = xmargin + col * scale
                x1 = xmargin + (col + 1) * scale
                y0 = ymargin + row * scale
                y1 = ymargin + (row + 1) * scale
                print(x0, y0, x1, y1)
                time.sleep(1)
                pygame.draw.rect(screen, WHITE, pygame.Rect(x0, y0, x1, y1))

                pygame.display.update()
    print("Donde")


# Game Variables
SQUARE_SIZE = 20
SCREEN_SIZE = (SQUARE_SIZE * 30, SQUARE_SIZE * 30)
SCREEN_CAPTION = "Mazing"
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Init Screen
os.environ["SDL_VIDEO_WINDOW_POS"] = "50,50"
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(SCREEN_CAPTION)
# pygame.display.set_icon(pygame.image.load(game.SCREEN_ICON))


maze = creator(10, 10, 35)
print_maze(maze)
draw_maze(maze)
