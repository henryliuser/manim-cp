res = []
while 1:
    s = input()
    if not s: break
    s = '"' + s + '"'
    res += [s]

for x in res: print(x)