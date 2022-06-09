import time

def valid(pw):
    v = False
    for i in range(len(pw) - 2):
        if pw[i + 1] == pw[i] + 1 and pw[i + 2] == pw[i] + 2:
            v = True
            break

    if not v:
        return False

    repeatCount = 0
    i = 0
    while i < len(pw) - 1:
        if pw[i] == pw[i + 1]:
            repeatCount += 1
            i += 1

        i += 1

    if repeatCount < 2:
        return False

    return True

def increment(pw):
    for i, c in enumerate(pw):
        if chr(c + ord('a')) in 'ilo':
            pw[i] += 1
            i += 1
            while i < len(pw):
                pw[i] = 0
                i += 1

            return pw

    ix = -1
    while abs(ix) <= len(pw):
        while True:
            pw[ix] += 1
            pw[ix] %= 26
            if chr(pw[ix] + ord('a')) not in 'ilo':
                break

        if pw[ix] == 0:
            ix -= 1
        else:
            break

    return pw

def main(data = 'cqjxjnds'):
    pw = increment([ord(c) - ord('a') for c in data])

    while not valid(pw):
        pw = increment(pw)

    print(f"\nPart 1:\nNew password: {''.join(chr(c + ord('a')) for c in pw)}")

    pw = increment(pw)

    while not valid(pw):
        pw = increment(pw)

    print(f"\nPart 2:\nNew password: {''.join(chr(c + ord('a')) for c in pw)}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main()
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
