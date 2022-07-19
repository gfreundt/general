def finder(n):
    remainder, used, num, last_is_zero = 1, [], 0, 0
    while True:
        remainder *= 10
        while n > remainder:
            remainder *= 10
            num += 1
            last_is_zero = 1
        use = remainder - (remainder // n) * n
        if use in used:
            return num - last_is_zero
        else:
            used.append(use)
            remainder = remainder % n
            num += 1
            last_is_zero = 0


a = finder(61043)
print(a)
