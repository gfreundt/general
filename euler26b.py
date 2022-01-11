def recurring_cycle(d):
    print("***************** d=", d)
    # solve 10^s % d == 10^(s+t) % d
    # where t is length and s is start
    for t in range(1, d):
        print(f"{t=}")
        if 10 ** t % d == 1:
            return t
    return 0


print(max(recurring_cycle(i) for i in range(2, 1000)) + 1)
