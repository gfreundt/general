with open('wap.txt', 'r', encoding='utf-8') as file:
    f=file.read()

g = {}
for char in list(set(f)):
    g.update({char:f.count(char)})

print(g)
