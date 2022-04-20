import pyautogui
import time
from copy import deepcopy as copy
from PIL import Image

import easyocr
import pytesseract

import itertools

pytesseract.pytesseract.tesseract_cmd = r"C:\pythonCode\Tesseract-OCR\tesseract.exe"


class Info:
    def __init__(self) -> None:
        self.centers = [
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
                "coords": (
                    i[0] - self.cut_size[0] // 2,
                    i[1] - self.cut_size[1] // 2,
                    i[0] + self.cut_size[0] // 2,
                    i[1] + self.cut_size[1] // 2,
                ),
            }
            for i in self.centers
        ]


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
        "RGB", (len(app.centers) * app.cut_size[0], app.cut_size[1]), (50, 50, 50)
    )

    # crop individual letters and paste to blank image (only 6 for now)
    for k, letter in enumerate(app.letters):
        croppedImage = img.crop((letter["coords"]))
        newImage.paste(croppedImage, (k * app.cut_size[0], 0))
    newImage.save(f"combo.jpg")

    # try two ocr methods, keep the best
    result1 = post_processing(
        easyocr.Reader(["en"]).readtext(
            "combo.jpg", paragraph=False, decoder="beamsearch"
        )[0][1]
    )
    result2 = post_processing(pytesseract.image_to_string(Image.open("combo.jpg")))
    return result1 if len(result1) == 6 else result2 if len(result2) == 6 else None


def go_thru_letters(word):
    temp_letters = copy(app.letters)
    print(f"{temp_letters=}")
    coords = []
    for letter in word:
        for k, c in temp_letters:
            print(f"{c=}")
            if letter == c["alpha"]:
                coords.append(c["coords"])
                temp_letters.pop(k)
    print(coords)
    return

    pyautogui.moveTo(app.centers[0][0], app.centers[0][1], 3)
    pyautogui.mouseDown(button="left")
    for c in range(1, len(app.centers)):
        pyautogui.moveTo(app.centers[c][0], app.centers[c][1], 1)
    pyautogui.mouseUp(button="left")


"""
1. Open App
2. Navigate to Game
3. Cut and identify letters
4. Create list of words
5. Click and drag each word, check for puzzle complete
6. Click for next puzzle
"""

# 0. Init
app = Info()

# 1. Open App
print("Starting in 5 seconds...")
# time.sleep(7)

# 2. Navigate to Game
# print("Navigate to Game")
# time.sleep(5)

# 3. Cut and identify letters, store them in dictionary with coordinates
# letters = [i.lower() for i in extract_letters()]
letters = [i.lower() for i in "estuta"]
for i, j in zip(app.letters, letters):
    i.update({"alpha": j})


# 4. Create list of words
words = []
for length in range(3, 7):
    words += ["".join(i) for i in itertools.permutations(letters, length) if len(i) > 2]
with open("english50k.txt", mode="r") as file:
    all_words = [i.strip() for i in file.readlines()]
possible_words = set([i for i in words if i in all_words])

print(sorted(possible_words, key=lambda i: len(i)))

# 5. Click and drag each word, check for puzzle complete
for word in possible_words:
    go_thru_letters(word)
