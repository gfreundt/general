from itertools import permutations as perm


def next_smaller(n):
    last = 2
    a = perm(str(n)[-n:])
    return a


print(next_smaller(7865439))
