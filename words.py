import pyautogui
import time
from PIL import Image

import easyocr
import pytesseract

import itertools

pytesseract.pytesseract.tesseract_cmd = r"C:\pythonCode\Tesseract-OCR\tesseract.exe"


def extract_letters():
    def post_processing(text):
        text = text.strip()
        text = text.replace("|", "I")
        text = text.replace("0", "O")
        text = text.replace(" ", "")
        text = "".join([i for i in text if i.isalpha()])
        return text

    cut_top_left = [
        (818, 652),
        (818, 778),
        (927, 839),
        (1030, 782),
        (1030, 652),
        (927, 590),
    ]
    cut_size = (70, 70)

    # take screenshot
    pyautogui.screenshot().save("screenshot.png")
    img = Image.open("screenshot.png")

    # create blank image
    newImage = Image.new(
        "RGB", (len(cut_top_left) * cut_size[0], cut_size[1]), (50, 50, 50)
    )

    for k, cds in enumerate(cut_top_left):
        croppedImage = img.crop(
            (cds[0], cds[1], cds[0] + cut_size[0], cds[1] + cut_size[1])
        )
        newImage.paste(croppedImage, (k * cut_size[0], 0))

    newImage.save(f"combo.jpg")
    # try two ocr methods, select the best
    result1 = post_processing(
        easyocr.Reader(["en"]).readtext(
            "combo.jpg", paragraph=False, decoder="beamsearch"
        )[0][1]
    )
    result2 = post_processing(pytesseract.image_to_string(Image.open("combo.jpg")))
    return result1 if len(result1) == 6 else result2 if len(result2) == 6 else None


def go_thru_letters(sequence):

    centers = [(853, 688), (853, 811), (960, 877), (1066, 811), (1066, 688), (960, 626)]
    centers = [
        (1215, 1124),
        (1215, 1303),
        (1365, 1384),
        (1522, 1303),
        (1522, 1124),
        (1365, 1034),
    ]
    pyautogui.moveTo(centers[0][0], centers[0][1], 3)
    pyautogui.mouseDown(button="left")
    for c in range(1, len(centers)):
        pyautogui.moveTo(centers[c][0], centers[c][1], 1)
        time.sleep(1)
    pyautogui.mouseUp(button="left")


"""
1. Open App
2. Navigate to Game
3. Cut and identify letters
4. Create list of words
5. Click and drag each word, check for puzzle complete
6. Click for next puzzle
"""


# 1. Open App
print("Starting in 5 seconds...")
time.sleep(7)

go_thru_letters(6)
quit()

# 2. Navigate to Game
# print("Navigate to Game")
# time.sleep(5)

# 3. Cut and identify letters
letters = [i.lower() for i in extract_letters()]
# letters = "ersune"

# 4. Create list of words
words = []
for length in range(3, 7):
    words += ["".join(i) for i in itertools.permutations(letters, length) if len(i) > 2]
# print(words)
with open("english479k.txt", mode="r") as file:
    all_words = [i.strip() for i in file.readlines()]
possible_words = set([i for i in words if i in all_words])

print(sorted(possible_words, key=lambda i: len(i)))
# print(words)
