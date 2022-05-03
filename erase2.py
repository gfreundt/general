import pyautogui
import opencv as cv2
import time


def check_for_jump():
    pyautogui.screenshot().save("screenshot.png")
    img = Image.open("screenshot.png")
    croppedImage = img.crop((850, 300, 1800, 500))
    croppedImage.save("temp.png")
    print(img)
    return True


def main():
    while True:
        if check_for_jump():
            pyautogui.press(" ")
            return


# start game
time.sleep(3)
pyautogui.press(" ")
main()
