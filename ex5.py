import itertools, math


def lP(word):
    """Return the anagram list position of the word"""
    letters = [i for i in word]
    p = list(sorted(set(["".join(i) for i in itertools.permutations(letters)])))
    return p.index(word) + 1


def listPosition(word):
    print("brute force:", lP(word))
    """Return the anagram list position of the word"""
    s = 0
    letters = [i for i in word]
    unique_letters = list(set(letters))
    for k, i in enumerate(letters):
        rl = sorted(letters[k:])
        p = rl.index(i)
        col = math.factorial(len(letters) - k - 1)
        s += p * col
    return s + 1


def listPosition(word):
    print("brute:", lP(word))
    """Return the anagram list position of the word"""
    letters = [i for i in word]
    return (
        sum(
            [
                sorted(letters[k:]).index(i) * math.factorial(len(letters) - k - 1)
                for k, i in enumerate(letters)
            ]
        )
        + 1
    )


print(listPosition("A"))
print(listPosition("ABCD"))
print(listPosition("AB"))
print(listPosition("AURELIO"))
print(listPosition("QUESTION"))
print(listPosition("BOOKKEEPER"))
