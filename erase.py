from math import factorial


def dec_2_fact_string(nb):
    r, leading = [], True
    for digits in range(36, -1, -1):
        c = nb // factorial(digits)
        if c >= 1:
            r.append(c)
            nb -= c * factorial(digits)
            leading = False
        elif not leading:
            r.append(c)
    return "".join([str(i) if i < 10 else chr(i + 55) for i in r])


def fact_string_2_dec(string):
    string = [int(i) if i.isdigit() else ord(i) - 55 for i in string]
    return sum(
        [factorial(len(string) - k) * int(i) for k, i in enumerate(string, start=1)]
    )


print(fact_string_2_dec("34145010"))

print(dec_2_fact_string(18247))
