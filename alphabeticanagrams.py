import itertools
from math import factorial, ceil


def score(word):
    def inorder(word):
        return sorted([i for i in word])

    dup = 1
    word = word.upper()
    score = 0
    for k, letter in enumerate(word):
        n = inorder(word[k:]).index(letter) * ceil(
            factorial(len(word) - k - 1) / factorial(dup)
        )
        score += n
    #        print(
    #            f"{inorder(word[k:]).index(letter)=} {factorial(len(word) - k - 1)=} {letter=}  {k=}  {n=}  {score=}"
    #        )

    return score + 1


# print(score("orange"))
# print(score("aegnor"))


testing = "agxzh"
# print(score(testing))
# quit()

test = sorted(set(["".join(j) for j in itertools.permutations([i for i in testing])]))
test2 = sorted(["".join(j) for j in itertools.permutations([i for i in testing])])

# test = ["ghxaza", "ghxzaa", "ghzaax", "ghzaxa"]


for k, t in enumerate(test, start=1):
    print(k, t, score(t), score(t) == k)
