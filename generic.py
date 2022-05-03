def dont_give_me_five(start, end):
    k = 0
    for i in range(start, end + 1):
        if "5" not in str(i):
            k += 1
    return k


for r in range(0, 100000, 1000):
    print(r, dont_give_me_five(r, r + 999))
