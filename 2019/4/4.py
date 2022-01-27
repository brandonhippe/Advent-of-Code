import math
import time

def arrtoInt(arr):
    val = 0
    for a in arr:
        val *= 10
        val += a
    
    return val

def foundP1(r):
    pw = [(r[0] // 10 ** i) % 10 for i in range(round(math.log10(r[0])))]
    pw.reverse()

    for i in range(len(pw) - 1):
        if pw[i + 1] < pw[i]:
            pw[i + 1] = pw[i]

    found = []
    if len(pw) != len(set(pw)):
        found.append(arrtoInt(pw))

    while True:
        for i in range(len(pw) - 1, -1, -1):
            if pw[i] != 9:
                pw[i] += 1
                i += 1
                break

        for j in range(i, len(pw)):
            pw[j] = pw[j - 1]

        if len(pw) == len(set(pw)):
            continue

        val = arrtoInt(pw)
        if val < r[1]:
            found.append(val)
        else:
            break

    return found

def foundP2(r):
    pw = [(r[0] // 10 ** i) % 10 for i in range(round(math.log10(r[0])))]
    pw.reverse()

    for i in range(len(pw) - 1):
        if pw[i + 1] < pw[i]:
            pw[i + 1] = pw[i]

    found = []

    groups = []
    size = 1
    for i in range(len(pw) - 1):
        if pw[i + 1] != pw[i]:
            groups.append(size)
            size = 1
        else:
            size += 1

    groups.append(size)

    if 2 in groups:
        found.append(arrtoInt(pw))

    while True:
        for i in range(len(pw) - 1, -1, -1):
            if pw[i] != 9:
                pw[i] += 1
                i += 1
                break

        for j in range(i, len(pw)):
            pw[j] = pw[j - 1]

        val = arrtoInt(pw)

        if val >= r[1]:
            break

        groups = []
        size = 1
        for i in range(len(pw) - 1):
            if pw[i + 1] != pw[i]:
                groups.append(size)
                size = 1
            else:
                size += 1

        groups.append(size)

        if 2 not in groups:
            continue

        if val < r[1]:
            found.append(val)

    return found

def main():
    r = [359282, 820401]    

    print(f"Part 1:\nNumber of valid passwords: {len(foundP1(r))}")
    print(f"Part 2:\nNumber of valid passwords: {len(foundP2(r))}")

init_time = time.perf_counter()
main()
print(f"\nRan in {time.perf_counter() - init_time} seconds")
