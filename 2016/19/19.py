import time

def p2(num):
    used = set()
    i = 1
    while len(used) < num - 1:
        steps = (num - len(used)) // 2
        n = i
        while steps > 0 or n in used:
            if n not in used:
                steps -= 1

            n %= num
            n += 1

        used.add(n)
        while True:
            i %= num
            i += 1
            if i not in used:
                break

    return i

def main(data = 3014603):
    print(f"\nPart 1:\nElf that steals all gifts: {int(bin(data)[3:] + bin(data)[2:3], 2)}")

    x = 1
    while x * 3 < data:
        x *= 3

    print(f"\nPart 2:\nElf that steals all gifts: {data - x if data <= 2 * x else x + 2 * (data - (2 * x))}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main()
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
