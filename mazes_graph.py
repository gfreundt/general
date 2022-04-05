from mazes import creator
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

    for r, row in enumerate(maze[:-1]):

        for c, cell in enumerate(row[:-1]):

            if maze[r][c + 1] == 1:
                pygame.draw.line(
                    screen,
                    WHITE,
                    (r * scale + xmargin, c * scale + ymargin),
                    (r * scale + xmargin, (c + 1) * scale + ymargin),
                )

            if maze[r + 1][c] == 1:
                pygame.draw.line(
                    screen,
                    WHITE,
                    (r * scale + xmargin, c * scale + ymargin),
                    ((r + 1) * scale + xmargin, c * scale + ymargin),
                )

    pygame.display.update()


# Game Variables
SQUARE_SIZE = 50
SCREEN_SIZE = (SQUARE_SIZE * 30, SQUARE_SIZE * 30)
SCREEN_CAPTION = "Mazing"
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Init Screen
os.environ["SDL_VIDEO_WINDOW_POS"] = "50,50"
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(SCREEN_CAPTION)
# pygame.display.set_icon(pygame.image.load(game.SCREEN_ICON))


maze = creator(10, 20, 50)
draw_maze(maze)
time.sleep(100)
