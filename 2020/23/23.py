import time

def main(data = 326519478):
    cups = [int(n) for n in str(data)]
    for _ in range(100):
        dest = cups[0] - 2
        dest %= len(str(data))
        while dest + 1 in cups[1:4]:
            dest -= 1
            dest %= len(str(data))

        dest = cups.index(dest + 1)
        cups = cups[4:dest + 1] + cups[1:4] + cups[dest + 1:] + [cups[0]]

    print(f"\nPart 1:\nDigits on cups after 1: {''.join(str(n) for n in cups[cups.index(1) + 1:] + cups[:cups.index(1)])}")

    cups = [int(n) for n in str(data)]
    cups = [cups[0]] + [cups[cups.index(i) + 1] if cups.index(i) < len(cups) - 1 else 10 for i in range(1, 10)] + [i + 1 for i in range(10, 1_000_000)] + [cups[0]]

    for _ in range(10_000_000):
        if (_ + 1) % 100_000 == 0:
            print(f"{(_ + 1) // 100_000}%", end='\r')

        held = cups[cups[0]]
        afterHeld = held
        removed = []
        for _ in range(3):
            removed.append(afterHeld)
            afterHeld = cups[afterHeld]

        dest = cups[0] - 2
        dest %= 1_000_000
        while dest + 1 in removed:
            dest -= 1
            dest %= 1_000_000

        afterDest = cups[dest + 1]

        cups[cups[0]] = afterHeld
        cups[dest + 1] = held
        cups[removed[-1]] = afterDest
        cups[0] = cups[cups[0]]

    print(f"\nPart 2:\nProduct of cups counterclockwise of 1: {cups[1] * cups[cups[1]]}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main()
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
