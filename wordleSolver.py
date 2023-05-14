import keyboard
import time
import itertools
import pyautogui
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as WebDriverOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


class Wordle:
    def __init__(self):
        # define variables
        self.allWords = [
            i.strip().upper() for i in open("wordleDictionary.txt", "r").readlines()
        ]
        a_to_z = [chr(i) for i in range(65, 91)]
        self.solvedWord = [list(a_to_z) for _ in range(5)]  # avoid using same memory
        self.presentLetters, self.absentLetters, self.solvedLetters = (
            set(),
            set(),
            set(),
        )
        self.rank = self.frequency()
        self.base_xpath = "/html/body/div[1]/div/section[1]/div/div[1]/div/div[1]/div/div/div[4]/div[6]/"
        self.buttons = [
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
            ["<", "Z", "X", "C", "V", "B", "N", "M", "@"],
        ]
        self.GREEN = [121, 184, 81]
        self.YELLOW = [243, 194, 55]
        self.GRAY = [164, 174, 196]
        self.tryWord = "AROSE"
        # define options for Chromedriver and open URL
        options = WebDriverOptions()
        options.add_argument("--silent")
        options.add_argument("--disable-notifications")
        options.add_argument("--incognito")
        options.add_argument("--log-level=3")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        web_url = "https://wordlegame.org/"
        self.webd = webdriver.Chrome(
            service=Service("C:\pythonCode\chromedriver.exe"), options=options
        )

        self.webd.set_window_position(1300, 0, windowHandle="current")
        self.webd.get(web_url)
        time.sleep(3)

    def frequency(self):
        count = [[chr(i), 0] for i in range(65, 91)]
        for word in self.allWords:
            for letter in word:
                i = ord(letter) - 65
                count[i][1] += 1
        return sorted(count, key=lambda i: i[1], reverse=True)

    def write(self, word):
        for letter in word:
            self.click_key(letter)
            time.sleep(2)
        self.click_key("@")
        time.sleep(2)

    def click_key(self, letter):
        line_text = [i for i in self.buttons if letter in i][0]
        line = self.buttons.index(line_text) + 1
        pos = line_text.index(letter) + 1
        self.webd.find_element(
            By.XPATH, f"{self.base_xpath}div[{line}]/div[{pos}]"
        ).click()

    def process_colors(self, position):
        top_left_row0 = (2656, 271)
        box_size = (93, 93)
        boxes = [
            pyautogui.screenshot(
                region=(
                    top_left_row0[0] + i * box_size[0],
                    top_left_row0[1] + position * box_size[1],
                    box_size[0],
                    box_size[1],
                )
            )
            for i in range(5)
        ]

        result = []

        G = [121, 184, 81]
        Y = [243, 194, 55]
        N = [164, 174, 196]

        for box in boxes:
            i = np.asarray(box)
            # print(i[80, 45])
            if np.array_equal(i[80, 45], self.GREEN):
                self.green_letter
            elif np.array_equal(i[80, 45], self.YELLOW):
                self.yellow_letter
            elif np.array_equal(i[80, 45], self.GRAY):
                self.gray_letter

        print(result)

    def green_letter(self, letter, position):
        self.solvedWord[position] = letter
        self.presentLetters.update(letter)
        self.solvedLetters.update(letter)

    def yellow_letter(self, letter, position):
        if letter in self.solvedWord[position]:
            self.solvedWord[position].remove(letter)
            self.presentLetters.update(letter)

    def gray_letter(self, letter):
        for pos, _ in enumerate(self.solvedWord):
            if letter in self.solvedWord[pos]:
                self.solvedWord[pos].remove(letter)
                self.absentLetters.update(letter)

    def get_possible_words(self):
        possible_words = [i for i in WORDLE.allWords if self.word_possible(i)]
        if len(possible_words) == 1:
            print(f"Solved with {possible_words[0]}")
            response_code = 1
        elif len(possible_words) == 0:
            print("Error!!")
            response_code = -1
        else:
            response_code = 0
        return (possible_words, response_code)

    def word_possible(self, word):
        w = list(word)
        # check if all present are there and all absent are not there
        for absent in self.absentLetters:
            if absent in w:
                return False
        for present in self.presentLetters:
            if present not in w:
                return False

        # test known positions
        for k, w in enumerate(self.solvedWord):
            if w and word[k] not in w:
                return False

        return True

    def get_next_best_word(self, wordList):
        scores = []
        for word in wordList:
            scores.append((word, self.calc_score(set(word), self.rank)))
        result = sorted(scores, key=lambda i: i[1], reverse=True)
        self.tryWord = result[0][0]

    def calc_score(self, option):
        score = 0
        for opt in option:
            i = [i[1] for i in self.rank if i[0] == opt][0]
            score += i
        return score

    """
    scores = []
    for word in allWords:
        scores.append((word, calc_score(set(word), rank)))
    scores = sorted(scores, key=lambda i: i[1], reverse=True)

    bestWords = list(itertools.permutations(top10Letters))
    result = []
    for i in tqdm(bestWords):
        a = "".join(i[:5])
        b = "".join(i[5:])
        if a in allWords and b in allWords:
            result.append((a, b, calc_score(a, rank)))

    print(result)
    result = sorted(result, key=lambda i: i[2], reverse=True)
    print(result)

    bestWords = list(itertools.permutations(next5Letters))
    result2 = []
    for i in tqdm(bestWords):
        a = "".join(i[:5])
        if a in allWords and b in allWords:
            result2.append((a))

    print(result2)
    return

    for k, first in enumerate(scores):
        for second in scores[k + 1 :]:
            print(set(list(first) + list(second)), set(top10Letters))
            if set(list(first) + list(second)) == set(top10Letters):
                print(first, second)
                return

    print(scores[:20])


def get_best_words(wordList):
    scores = []
    for word in wordList:
        scores.append((word, calc_score(set(word), rank)))
    result = sorted(scores, key=lambda i: i[1], reverse=True)
    return [i[0] for i in result[:5]]


def get_one_key_response(valid_responses):
    start = time.perf_counter()
    while True:
        letter = keyboard.read_key(suppress=True).upper()
        if letter in valid_responses and time.perf_counter() - start > 0.2:
            return letter


def word_possible(word):
    w = list(word)
    # check if all present are there and all absent are not there
    for absent in absentLetters:
        if absent in w:
            return False
    for present in presentLetters:
        if present not in w:
            return False

    # test known positions
    for k, w in enumerate(solvedWord):
        if w and word[k] not in w:
            return False

    return True
    """


def main():
    turn = 0
    while turn <= 5:
        WORDLE.write(WORDLE.tryWord)
        WORDLE.process_colors(turn)
        possible_words, response_code = WORDLE.get_possible_words()
        if response_code:
            print("The End")
            break
        WORDLE.get_next_best_word(possible_words)
        turn += 1

    return

    while turns < 6:
        print(f"Trying: {best_score_word}\n")
        WORDLE.write(best_score_word)

    return


"""


        test_word = input("Enter Test Word: ").upper()

        print("Valid answers: (G)reen, (Y)ellow, (N)one\n")
        valid_response = ("G", "Y", "N")

        for k, letter in enumerate(test_word):
            print(f"Result for {letter}: ", end="", flush=True)
            status = (
                get_one_key_response(valid_response)
                if letter not in solvedLetters
                else "G"
            )
            print()
            if status == "G":
                green_letter(letter, k)
            elif status == "Y":
                yellow_letter(letter, k)
            elif status == "N":
                gray_letter(letter)

            # print(f"{presentLetters=}, {absentLetters=}")
            # print(f"{solvedWord=}")

        possible_words = [i for i in allWords if word_possible(i)]
        # print(possible_words)

        if len(possible_words) == 1:
            print(f"Answer: {possible_words[0]}")
            break
        elif len(possible_words) == 0:
            print("Error!!")
            break

        best_score_word = get_best_words(possible_words)
        print(best_score_word)

        turns += 1


allWords = [i.strip().upper() for i in open("wordleDictionary.txt", "r").readlines()]
a_to_z = [chr(i) for i in range(65, 91)]
solvedWord = [list(a_to_z) for _ in range(5)]  # to avoid using same memory position
presentLetters, absentLetters, solvedLetters = set(), set(), set()
rank = frequency()

# main()
"""
for i in range(0, 1):
    get_colors(i)

quit()
WORDLE = Wordle()
main()
