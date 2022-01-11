def diophantine(D, start):
    print(f"{start=}")
    for x in range(start, start + 10000):
        for y in range(start, start + 10000):
            if x ** 2 - D * y ** 2 == 1:
                return x, y


def dio(D):
    x = 2
    while True:
        y = ((x ** 2 - 1) / D) ** 0.5
        if y - int(y) == 0:
            return x, int(y)
        else:
            x += 1


maxx = 0
for i in range(2, 1001):
    print(i)
    if i ** 0.5 - int(i ** 0.5) != 0:
        x, y = dio(i)
        if x > maxx:
            maxx = int(x)
            maxD = int(i)

print(f"Max D = {maxD}")
