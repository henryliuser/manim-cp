from random import randint as rng
from random import shuffle
N = int( input() )

def checkStr8(A):
    for i in range(10):
        if all(A[j%13] for j in range(i, i+5)):
            return True
    return False

def pick(A, left):
    r = rng(0, left-1)
    A[r], A[-1] = A[-1], A[r]
    return A.pop()

def sim():
    CARDS = [*range(52)]
    shuffle(CARDS)
    flush = [0] * 4
    str8  = [0] * 13
    FLUSH = STR8 = False
    cnt = [0,0]
    while True:
        r = CARDS.pop()
        if not FLUSH: cnt[0] += 1
        if not STR8:  cnt[1] += 1
        s = r // 13  # suite index
        v = r % 13   #
        flush[s] += 1
        str8[v] = 1
        FLUSH = any(x >= 5 for x in flush)
        STR8  = checkStr8(str8)
        if FLUSH and STR8: return cnt

win = [0] * 3
avg = [0] * 3
for _ in range(N):
    cnt = sim()
    w = 1 if cnt[1] < cnt[0] else 0 if cnt[0] < cnt[1] else 2
    win[w] += 1
    for j in [0,1]:
        avg[j] += cnt[j]

print(win)
for i in [0,1]:
    print(f"{avg[i] / N:.5f}")