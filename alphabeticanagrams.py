import itertools
from math import factorial
from os import dup


def score(word):
    def inorder(word):
        return sorted([i for i in word])

    dup = 4
    word = word.upper()
    score = 0
    for k, letter in enumerate(word):
        score += (
            inorder(word[k:]).index(letter)
            * factorial(len(word) - k - 1)
            // factorial(dup)
        )
    return score + 1


# print(score("orange"))
# print(score("aegnor"))


testing = "agaxzaa"
# print(score(testing))
# quit()

test1 = sorted(set(["".join(j) for j in itertools.permutations([i for i in testing])]))
test2 = sorted(["".join(j) for j in itertools.permutations([i for i in testing])])


for k, t in enumerate(test1, start=1):
    print(k, t, score(t))
