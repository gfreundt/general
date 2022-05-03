def look_and_say(data="1", maxlen=5):
    r = []
    for _ in range(maxlen):
        data = interpreter(data)
        r.append(data)
    return r


def interpreter(data):
    r = ""
    multip = 1
    pos = 0
    while True:
        if pos == len(data) - 1:
            r += str(multip) + data[pos]
            break
        elif data[pos] == data[pos + 1]:
            multip += 1
            pos += 1
        else:
            r += str(multip) + data[pos]
            pos += 1
            multip = 1
    return r


a = look_and_say()

print(a)


"""     1
         11
         21
        1211
       111221
       312211
      13112221
     1113213211
     
"""
