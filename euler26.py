import decimal
from tqdm import tqdm

decimal.getcontext().prec = 1000


def cycle(n):
    # only decimal part
    n = n.split(".")[1]
    # remove leading zeroes
    while n[0] == "0":
        n = n[1:]

    for chunk_size in range(1, 999):
        for startpos, _ in enumerate(n):
            chunks = [
                n[startpos + chunk_size * i : startpos + chunk_size * (i + 1)]
                for i in range(3)
            ]

            if chunks.count(chunks[0]) == len(chunks):
                return chunks[0], len(chunks[0])
    return "", 0


max_recip_len = 0
for i in tqdm(range(2, 1000)):
    g = str(decimal.Decimal(1) / decimal.Decimal(i))
    recip, rlen = cycle(g)
    print(f"Fraction: 1/{i} = {g} -- Reciprocal = {recip} -- Length = {rlen}")
    if rlen > max_recip_len:
        max_recip_len = int(rlen)
        max_no = int(i)

print(max_no, max_recip_len)
