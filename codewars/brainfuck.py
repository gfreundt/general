def brain_luck(code, program_input):
    # parse code to find matching parenthesis pairs and store them in dictionaries
    n, k, t = 0, 0, -1
    pars = [[] for _ in range(code.count("["))]
    for n, c in enumerate(code):
        if c == "[":
            t += 1
            pars[t].append(n)
            k = t

        elif c == "]":
            pars[k].append(n)
            k -= 1

    print(pars)
    open_pars = {pars[k][0]: pars[k][1] for k, _ in enumerate(pars)}
    close_pars = {open_pars[i]: i for i in open_pars}

    # define initial values
    ip, dp = 0, -1
    mem = [0] * 10
    pinput = list(program_input)
    output = ""

    # loop thru code and execute instructions
    while ip < len(code):
        if code[ip] == ">":
            ip += 1
        elif code[ip] == "<":
            ip -= 1
        elif code[ip] == "+":
            mem[dp] = mem[dp] + 1 if mem[dp] < 255 else 0
            ip += 1
        elif code[ip] == "-":
            mem[dp] = mem[dp] - 1 if mem[dp] > 0 else 255
            ip += 1
        elif code[ip] == ".":
            output += chr(mem[dp])
            ip += 1
        elif code[ip] == ",":
            dp += 1
            mem[dp] = ord(pinput.pop(0))
            ip += 1
        elif code[ip] == "[":
            if mem[dp] == 0:
                ip = open_pars[ip] + 1
            else:
                ip += 1
        elif code[ip] == "]":
            if mem[dp] == 0:
                ip += 1
            else:
                ip = close_pars[ip] + 1

    return output


# v = brain_luck(",[.[-],]", "Codewars" + chr(0))
# v = brain_luck(",+[-.,+]", "Codewars" + chr(255))
v = brain_luck(",>,<[>[->+>+<<]>>[-<<+>>]<<<-]>>.", chr(8) + chr(9))
print(v)
