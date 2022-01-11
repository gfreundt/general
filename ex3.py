class Supersum:
    def __init__(self) -> None:
        self.result = []


def exp_sum(n):
    # global supersum
    # supersum = Supersum()
    recursive(n, n, [])
    return len(set(tuple(i) for i in supersum.result))


def recursive(n, N, test):
    if n == 0:
        return test
    for i in range(n + 1):
        test.append(i)
        if sum(test) == N and len(test) == N:
            supersum.result.append(sorted(test))
        elif sum(test) > N:
            return test[:-1]
        test = recursive(n - 1, N, test)
        test = test[:-1]
    return test


supersum = Supersum()
for i in range(1, 10):
    print(f"{i} = {exp_sum(i)}")
    supersum.result = []
