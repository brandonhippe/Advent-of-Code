from time import perf_counter


dirs = {"L": (-1, 0), "R": (1, 0), "U": (0, 1), "D": (0, -1)}


def manhatDist(p1, p2):
    return sum(abs(c1 - c2) for c1, c2 in zip(p1, p2))


def moveTail(head, tail):
    if (any(h == t for h, t in zip(head, tail)) and max(abs(h - t) for h, t in zip(head, tail)) == 2) or manhatDist(head, tail) >= 3:
        diff = [((h - t) // abs(h - t)) if h - t != 0 else 0 for h, t in zip(head, tail)]
        return [c1 + c2 for c1, c2 in zip(tail, diff)]
    else:
        return tail


def main(verbose):
    with open("input.txt", encoding="UTF-8") as f:
        lines = [line.strip('\n') for line in f.readlines()]

    head = [0, 0]
    tail = [0, 0]
    tailVisits = set()

    for line in lines:
        d, amt = line.split(' ')
        d = dirs[d]
        amt = int(amt)

        while amt > 0:
            head = [p + o for p, o in zip(head, d)]

            tailVisits.add(tuple(tail))
            tail = moveTail(head, tail)

            amt -= 1

    tailVisits.add(tuple(tail))
    part1 = len(tailVisits)

    tails = [[0, 0] for _ in range(10)]
    tailVisits = set()

    for line in lines:
        d, amt = line.split(' ')
        d = dirs[d]
        amt = int(amt)

        while amt > 0:
            tails[0] = [t + o for t, o in zip(tails[0], d)]

            tailVisits.add(tuple(tails[-1]))
            for i in range(1, 10):
                tails[i] = moveTail(tails[i - 1], tails[i])

            amt -= 1

    tailVisits.add(tuple(tail))

    if verbose:
        print(f"\nPart 1:\nNumber of positions visited by tail of rope: {part1}\n\nPart 2:\nNumber of positions visited by tail of rope: {len(tailVisits)}")

    return [part1, len(tailVisits)]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")