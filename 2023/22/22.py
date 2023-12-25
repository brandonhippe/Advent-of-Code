from time import perf_counter
import re
from collections import defaultdict, deque


def intersect(x1, y1, x2, y2, x3, y3, x4, y4):
    if x2 < x3:
        return False
    
    if x4 < x1:
        return False
    
    if y2 < y3:
        return False
    
    if y4 < y1:
        return False
    
    return True


def fall(bricks):
    newBricks = []
    for c1, c2 in bricks:
        zHeight = c2[-1] - c1[-1]

        newZ = 1
        for c3, c4 in newBricks:
            if not intersect(*c1[:-1], *c2[:-1], *c3[:-1], *c4[:-1]):
                continue

            newZ = max(newZ, c4[-1] + 1)

        newBricks.append((tuple(list(c1[:-1]) + [newZ]), tuple(list(c2[:-1]) + [newZ + zHeight])))

    return sorted(newBricks, key=lambda b: b[0][-1])


def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    bricks = sorted([[[int(n) for n in re.findall('\d+', l)] for l in line.split('~')] for line in lines], key=lambda b: b[0][-1])
    bricks = fall(bricks)

    support = defaultdict(lambda: [])
    supportedBy = defaultdict(lambda: [])

    for i, (c1, c2) in enumerate(bricks):
        for c3, c4 in bricks[i + 1:]:
            if c3[-1] > c2[-1] + 1:
                break

            if c3[-1] == c2[-1] + 1 and intersect(*c1[:-1], *c2[:-1], *c3[:-1], *c4[:-1]):
                support[(c1, c2)].append((c3, c4))
                supportedBy[(c3, c4)].append((c1, c2))

    chain = set()
    disintegrate = set(bricks)
    for b in supportedBy.values():
        if len(b) != 1:
            continue

        b = b[0]
        if b in disintegrate:
            chain.add(b)
            disintegrate.remove(b)

    part1 = len(disintegrate)

    part2 = 0
    for b in chain:
        fallen = set()
        toFall = deque()
        for b1 in support[b]:
            if len(supportedBy[b1]) == 1:
                toFall.append(b1)

        while len(toFall) != 0:
            b1 = toFall.popleft()
            fallen.add(b1)

            for b2 in support[b1]:
                if all(s in fallen or s == b for s in supportedBy[b2]):
                    toFall.append(b2)

        part2 += len(fallen)

    if verbose:
        print(f"\nPart 1:\nNumber of safe bricks: {part1}\n\nPart 2:\nTotal number of falling bricks:{part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")
