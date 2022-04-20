import pyautogui
import time
import platform
from copy import deepcopy as copy
from PIL import Image

import easyocr
import pytesseract as pyt

from itertools import permutations


class Info:
    def __init__(self) -> None:
        centers = [
            (1215, 1124),
            (1215, 1303),
            (1365, 1384),
            (1522, 1303),
            (1522, 1124),
            (1365, 1034),
        ]
        # self.centers = [(853, 688), (853, 811), (960, 877), (1066, 811), (1066, 688), (960, 626)]
        self.cut_size = (70, 70)
        self.letters = [
            {
                "alpha": " ",
                "centers": i,
                "edges": (
                    i[0] - self.cut_size[0] // 2,
                    i[1] - self.cut_size[1] // 2,
                    i[0] + self.cut_size[0] // 2,
                    i[1] + self.cut_size[1] // 2,
                ),
            }
            for i in centers
        ]
        self.dial_center = (centers[2][0], (centers[0][1] + centers[1][1]) // 2)
        self.slide_time = 0.2
        self.drive = "D:" if platform.node() == "power" else "C:"


def extract_letters():
    def post_processing(text):
        text = text.strip()
        text = text.replace("|", "I")
        text = text.replace("0", "O")
        text = text.replace(" ", "")
        text = "".join([i for i in text if i.isalpha()])
        return text

    # take screenshot
    pyautogui.screenshot().save("screenshot.png")
    img = Image.open("screenshot.png")

    # create blank image
    newImage = Image.new(
        "RGB", (len(app.letters) * app.cut_size[0], app.cut_size[1]), (50, 50, 50)
    )

    # crop individual letters and paste to blank image (only 6 for now)
    for k, letter in enumerate(app.letters):
        croppedImage = img.crop((letter["edges"]))
        newImage.paste(croppedImage, (k * app.cut_size[0], 0))
    newImage.save(f"combo.jpg")

    # try two ocr methods, keep the best
    result1 = post_processing(
        easyocr.Reader(["en"]).readtext(
            "combo.jpg", paragraph=False, decoder="beamsearch"
        )[0][1]
    )
    result2 = post_processing(pyt.image_to_string(Image.open("combo.jpg")))
    result = result1 if len(result1) == 6 else result2 if len(result2) == 6 else None
    return list(result.lower()) if result else None


def get_valid_words(letters):
    words = []
    for length in range(3, 7):
        words += ["".join(i) for i in permutations(letters, length) if len(i) > 2]
    with open("english50k.txt", mode="r") as file:
        all_words = [i.strip() for i in file.readlines()]
    return sorted(set([i for i in words if i in all_words]), key=lambda i: len(i))


def go_thru_letters(word):
    # get coordinates for sequence of letters
    temp_letters = copy(app.letters)
    coords = []
    for letter in word:
        for k, c in enumerate(temp_letters):
            if letter == c["alpha"]:
                coords.append(c["centers"])
                temp_letters.pop(k)
                break
    # click thru sequence of letter coordinates on app
    pyautogui.moveTo(coords[0][0], coords[0][1], app.slide_time)
    pyautogui.mouseDown(button="left")
    for c in coords[1:]:
        pyautogui.moveTo(c[0], c[1], app.slide_time)
    pyautogui.mouseUp(button="left")
    pyautogui.moveTo(app.dial_center[0], app.dial_center[1], app.slide_time)


# 0. Init
app = Info()
pyt.pytesseract.tesseract_cmd = rf"{app.drive}\pythonCode\Tesseract-OCR\tesseract.exe"

# 1. Open App
print("Starting in 5 seconds...")
time.sleep(5)

# 2. Navigate to Game
# print("Navigate to Game")
# time.sleep(5)

# 3. Cut and identify letters, store them in dictionary with coordinates
letters = extract_letters()
# letters = list("estuta")
for i, j in zip(app.letters, letters):
    i.update({"alpha": j})


# 4. Create list of words
valid_words = get_valid_words(letters)


# 5. Click and drag each word, check for puzzle complete
for word in valid_words:
    print(word)
    go_thru_letters(word)
    time.sleep(1)
