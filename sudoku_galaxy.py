import pyautogui
import time
import platform
from copy import deepcopy as copy
from PIL import Image, ImageGrab
import numpy as np
from tqdm import tqdm

import easyocr
import pytesseract as pyt

from itertools import permutations

from sudoku import Sudoku


class Info:
    def __init__(self) -> None:
        self.grid_top_left = (245, 85)
        self.grid_box_size = 100
        self.grid_box_inside_margin = 10
        self.grid_digit_cutouts = [
            (
                self.grid_top_left[0]
                + self.grid_box_size * i
                + self.grid_box_inside_margin,
                self.grid_top_left[1]
                + self.grid_box_size * j
                + self.grid_box_inside_margin,
                self.grid_top_left[0]
                + self.grid_box_size * (i + 1)
                - self.grid_box_inside_margin,
                self.grid_top_left[1]
                + self.grid_box_size * (j + 1)
                - self.grid_box_inside_margin,
            )
            for j in range(9)
            for i in range(9)
        ]

        self.grid_centers = [
            (
                self.grid_top_left[0] + int(self.grid_box_size * (j + 0.5)),
                self.grid_top_left[1] + int(self.grid_box_size * (i + 0.5)),
            )
            for i in range(9)
            for j in range(9)
        ]

        self.pad_top_left = (1450, 320)
        self.pad_box_hsize = 100
        self.pad_box_vsize = 150
        self.pad_centers = [
            (
                self.pad_top_left[0] + int(self.pad_box_hsize * j),
                self.pad_top_left[1] + int(self.pad_box_vsize * i),
            )
            for i in range(3)
            for j in range(3)
        ]

        self.drive = "D:" if platform.node() == "power" else "C:"


def extract_letters():
    def is_blank(img):
        for i in cutout:
            for j in i:
                for k in j:
                    if k < 200:
                        return False
        return True

    def post_processing(ocr_response):
        ocr_response = ocr_response[0][1] if ocr_response else "0"
        ocr_response = ocr_response.strip()
        ocr_response = ocr_response.replace("I", "1")
        ocr_response = ocr_response.replace("O", "0")
        return int(ocr_response)

    # take screenshot
    img = ImageGrab.grab()
    result = []
    # OCR one by one
    for digit in tqdm(app.grid_digit_cutouts):
        cutout = np.asarray(img.crop(digit))
        if is_blank(cutout):
            ocr_digit = 0
        else:
            ocr_digit = post_processing(
                easyocr.Reader(["en"], verbose=False).readtext(
                    image=cutout,
                    paragraph=False,
                    decoder="greedy",
                    text_threshold=0.4,
                )
            )
        result.append(ocr_digit)
    return [[i for i in result[j * 9 : (j + 1) * 9]] for j in range(9)]


def insert_missing_digits(solved_puzzle, original_puzzle):
    def point_and_click(pos, digit):
        # move to grid square and click
        x, y = app.grid_centers[pos]
        pyautogui.moveTo(x, y, 0.2)
        pyautogui.click()
        # move to number in pad and click
        x, y = app.pad_centers[digit - 1]
        pyautogui.moveTo(x, y, 0.2)
        pyautogui.click()
        # pyautogui.click(x, y)

    # create grid with solutions to initial empty puzzle positions
    missing_digits = [
        j if not original_puzzle[m][n] else 0
        for m, i in enumerate(solved_puzzle)
        for n, j in enumerate(i)
    ]

    # fill all empty spaces left to right, top to bottom
    for pos, digit in enumerate(missing_digits):
        if digit:
            point_and_click(pos, digit)


def test():
    result = [
        0,
        0,
        7,
        0,
        4,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        8,
        0,
        0,
        6,
        0,
        4,
        1,
        0,
        0,
        0,
        9,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        7,
        0,
        0,
        0,
        0,
        0,
        0,
        6,
        0,
        0,
        0,
        0,
        0,
        8,
        7,
        0,
        0,
        2,
        0,
        0,
        3,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        2,
        0,
        0,
        0,
        0,
        8,
        6,
        0,
        0,
        7,
        0,
        0,
        0,
        5,
    ]
    print(result)
    print([[i for i in result[j * 9 : (j + 1) * 9]] for j in range(9)])


# 0. Init
# drive = "D:" if platform.node() == "power" else "C:"
print("Starting in 5 seconds...")
time.sleep(5)

# 1. Open App and Navigate to Game

while True:
    app = Info()

    original_puzzle = [
        [0, 0, 7, 0, 4, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 8, 0, 0, 6],
        [0, 4, 1, 0, 0, 0, 9, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 7, 0],
        [0, 0, 0, 0, 0, 6, 0, 0, 0],
        [0, 0, 8, 7, 0, 0, 2, 0, 0],
        [3, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 2, 0, 0, 0, 0],
        [8, 6, 0, 0, 7, 0, 0, 0, 5],
    ]
    original_puzzle = extract_letters()
    print(original_puzzle)
    solved_puzzle = Sudoku(3, 3, board=original_puzzle).solve().board
    print(solved_puzzle)
    insert_missing_digits(solved_puzzle, original_puzzle)
    quit()

    # 2. Clear bonus words
    pyautogui.click(x=1110, y=245, clicks=1, button="left")  # click on bonus icon
    time.sleep(2)
    pyautogui.click(x=1380, y=1370, clicks=1, button="left")  # click "claim"
    time.sleep(2)
    pyautogui.click(x=1380, y=1490, clicks=1, button="left")  # click "back to puzzle"

    # 3. Cut and identify letters, store them in dictionary with coordinates
    letters, k = None, 0
    while not letters:
        letters = extract_letters()
        if not letters:
            pyautogui.click(x=1010, y=245, clicks=1, button="left")
            k += 1
            if k > 2:
                print("stopped!")
                quit()

    for i, j in zip(app.letters, letters):
        i.update({"alpha": j})

    # 4. Create list of words
    valid_words = get_valid_words(letters)

    # 5. Click and drag each word, click "NEXT"
    for word in valid_words:
        print(word)
        go_thru_letters(word)
    time.sleep(12)  # wait for animation and "next" to appear
    pyautogui.click(x=1380, y=1370, clicks=1, button="left")
    time.sleep(1)
    pyautogui.moveTo(1000, 1000, 0.2)  # move cursor out of the way for next screenshot
    time.sleep(5)  # wait for puzzle to load
