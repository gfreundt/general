import numpy as np
from PIL import Image, ImageGrab
import pyautogui
import time, os
import csv
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as WebDriverOptions


class Game:
    def __init__(self) -> None:
        self.app_parameters = {
            "cornerx": 0,
            "cornery": 103,
            "sizex": 108,
            "sizey": 108,
            "offset": 20,
            "guide": self.load_pieces("guide_app.txt"),
            "init_board_file": "app_init_board.jpg",
            "img_size": 68,
        }
        self.web_parameters = {
            "cornerx": 576,
            "cornery": 163,
            "sizex": 92,
            "sizey": 92,
            "offset": 18,
            "guide": self.load_pieces("guide_web.txt"),
            "init_board_file": "web_init_board.jpg",
            "img_size": 56,
        }
        self.web_url = "https://lichess.org/"
        self.webdriver = self.load_webdriver()

    def load_pieces(self, filename):
        with open(filename, mode="r") as file:
            d = csv.reader(file)
            return [
                {"piece": line[0], "index": int(line[1]), "margin": int(line[2])}
                for line in d
            ]

    def load_webdriver(self):
        """Define options for Chromedriver"""
        options = WebDriverOptions()
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--silent")
        options.add_argument("--disable-notifications")
        options.add_argument("--incognito")
        options.add_argument("--log-level=3")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        return webdriver.Chrome(
            os.path.join(r"C:\pythonCode", "chromedriver.exe"),
            options=options,
        )

    def focus_window(self, interface):
        if interface == "app":
            pyautogui.press("win")
            time.sleep(0.5)
            pyautogui.write("dex")
            pyautogui.press("enter")
            time.sleep(2)
        elif interface == "web":
            pyautogui.getWindowsWithTitle("Chrome")[0].minimize()
            pyautogui.getWindowsWithTitle("Samsung DeX")[0].minimize()
            time.sleep(1)
            pyautogui.getWindowsWithTitle("Samsung DeX")[0].maximize()
            pyautogui.getWindowsWithTitle("Chrome")[0].maximize()
            time.sleep(2)

    def web_start(self, color, strength=6):
        # open URL and focus on browser
        self.webdriver.get(GAME.web_url)
        time.sleep(1)
        self.focus_window("web")
        time.sleep(1)
        # Press PLAY WITH THE COMPUTER
        self.webdriver.find_element_by_xpath(
            "/html/body/div/main/div[1]/div[2]/a[3]"
        ).click()
        time.sleep(2)
        # select Strength
        pyautogui.click(830 + 37 * (strength - 1), 620)
        time.sleep(1)
        # select Color
        pyautogui.click(850 + (220 * color), 770)
        time.sleep(4)
        # flip board
        pyautogui.click(1365, 455)
        time.sleep(2)

    def alt_tab(self, turn):
        pyautogui.keyDown("alt")
        time.sleep(0.2)
        pyautogui.press("tab")
        time.sleep(0.2)
        pyautogui.keyUp("alt")
        # return new window parameters
        return (
            self.web_parameters if turn == self.app_parameters else self.app_parameters
        )


def board_analysis(parameters, setup=False, init_board=False):
    cornerx, cornery = parameters["cornerx"], parameters["cornery"]
    sizex, sizey = parameters["sizex"], parameters["sizey"]
    offset = parameters["offset"]
    board = []
    screenshot = (
        Image.open(parameters["init_board_file"]).convert("L")
        if init_board
        else ImageGrab.grab().convert("L")
    )
    for y in range(8):
        for x in range(8):
            img = screenshot.crop(
                (
                    cornerx + sizex * x + offset,
                    cornery + sizey * y + offset,
                    cornerx + sizex * (x + 1) - offset,
                    cornery + sizey * (y + 1) - offset,
                )
            )
            piece_name = get_piece(img, parameters["guide"], parameters["img_size"])
            # print("piece", piece_name)
            if not piece_name:
                return None
            if setup:  # only runs once to determine which color we are playing with
                return piece_name[0]
            board.append(piece_name)
    return board


def get_piece(img, guide, img_size):
    # process image
    pimg = np.array([[0 if i < 130 else 255 for i in j] for j in np.asarray(img)])
    pimg = np.asarray(Image.fromarray(pimg).convert("1"))
    # get sample
    n = 0
    for i in range(0, img_size, 3):
        n += sum([pimg[i][j] for j in range(img_size)])
        n += sum([pimg[j][i] for j in range(img_size)])
    # determine which piece
    for g in guide:
        if g["index"] - g["margin"] <= n <= g["index"] + g["margin"]:
            return g["piece"]
    # piece not identified
    return None


def move(turn, coords):
    (x0, y0), (x1, y1) = coords
    pyautogui.moveTo(
        turn["cornerx"] + turn["sizex"] * x0 + turn["offset"] * 2,
        turn["cornery"] + turn["sizey"] * y0 + turn["offset"] * 2,
        random.randint(1, 30) / 10,
    )
    pyautogui.mouseDown(button="left")
    pyautogui.moveTo(
        turn["cornerx"] + turn["sizex"] * x1 + turn["offset"] * 2,
        turn["cornery"] + turn["sizey"] * y1 + turn["offset"] * 2,
        random.randint(1, 30) / 10,
    )
    pyautogui.mouseUp(button="left")


def coord(n):
    return (n % 8, n // 8)


def print_board(board):
    dashes = "-" * 41 + "\n"
    b = dashes
    for y in range(8):
        line = "|"
        for x in range(8):
            line += " " + board[y * 8 + x] + " |"
        b += line + "\n" + dashes
    print(b)


def loop_until_board_changes(turn, init_board=False):
    # loop until it gets a valid initial board unless it's initial board
    if init_board and turn == 0:
        previous_board = board_analysis(turn, init_board=True)
    else:
        previous_board = None
        while not previous_board:
            previous_board = board_analysis(turn)
    # loop until there is a change in board (move)
    while True:
        time.sleep(1)
        board = board_analysis(turn)
        if board and previous_board != board:
            # there are changes (player moved piece)
            move = []
            for k, _ in enumerate(board):
                if board[k] != previous_board[k]:
                    move.append(k)
            print_board(board)
            return (
                (coord(move[0]), coord(move[1]))
                if move[0] == "  "
                else (coord(move[1]), coord(move[0]))
            )


"""
colors: 0 = white, 1 = black
"""


time.sleep(5)
st = time.perf_counter()
GAME = Game()

# switch to app and determine color we are playing
GAME.focus_window("app")
color = 0 if board_analysis(GAME.app_parameters, setup=True) == "b" else 1

# open browser and start website, select strength and color, flip board
GAME.web_start(color)

# select which interface to start on (white on app = start on web)
if color == 0:
    turn = GAME.web_parameters
    GAME.focus_window("web")
else:
    turn = GAME.app_parameters
    GAME.focus_window("app")

quit()


init_board = True
while True:
    print(turn)
    # wait until opponent moves
    opp_move = loop_until_board_changes(turn, init_board)
    init_board = False
    # replicate opponent's move in other interface
    turn = GAME.alt_tab(turn)
    # time.sleep(1)
    # move(turn, coords=opp_move)
