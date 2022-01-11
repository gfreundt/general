from tqdm import tqdm
import time

start = time.time()


def is_prime(n):
    # if n % 2 == 0:
    #     return False
    for i in range(3, int(n / 2) + 1, 2):
        if n % i == 0:
            return False
    return True


def factors(n):
    if n in prime_list:
        return [n]
    factors = []
    # avoiding 1 on purpose
    for f in prime_list:
        while True:
            if n % f == 0:
                factors.append(f)
                n = n / f
                if n == 1:
                    return list(set(factors))
            else:
                break


def relative_primes(n, m):
    factorsn = factor_list[n]
    factorsm = factor_list[m]
    for i in factorsn:
        if i in factorsm:
            return False
    return True


def phi(n):
    return len([1] + [i for i in range(2, n) if relative_primes(i, n)])


def is_permutation(n, m):
    n, m = list(str(n)), list(str(m))
    if len(n) != len(m):
        return False
    if sorted(n) == sorted(m):
        print(n, m)
        return True
    return False


run = 10 ** 7

with open("primes.txt", mode="r") as file:
    primes = [int(i) for i in file]

# prime_list = [2] + [i for i in tqdm(range(3, run, 2)) if is_prime(i)]
# print(f"[{time.time()-start}] Prime List Generation Complete")
# with open("primes.txt", mode="w") as outfile:
#    for item in prime_list:
#        outfile.write(str(item) + "\n")

factor_list = {i: factors(i) for i in tqdm(range(2, run))}
print(f"[{time.time()-start}] Factor List Generation Complete")
quit()
for i in tqdm(range(3, 5000)):
    p = phi(i)
    if is_permutation(i, p):
        print(i, p)

print(f"Time: {time.time() - start} sec")
