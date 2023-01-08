from time import perf_counter
import re

def main(verbose):
    with open("input.txt", encoding="UTF-8") as f:
        lines = [line.strip('\n') for line in f.readlines()]

    area = set()
    for line in lines:
        nums = [int(x) for x in re.findall("\d+", line)]

        pos = tuple(nums[:2])

        for i in range(2, len(nums), 2):
            offset = [(abs(n - p) // (n - p)) if n - p != 0 else 0 for p, n in zip(pos, nums[i:i + 2])]

            while pos != tuple(nums[i:i + 2]):
                area.add(pos)
                pos = tuple(p + o for p, o in zip(pos, offset))

        area.add(pos)

    maxY = max([e[1] for e in list(area)]) + 1

    pastPos = [(500, 0)]
    sand = set()
    sandP1 = None

    while len(pastPos) != 0:
        pos = pastPos.pop()

        if pos[1] == maxY:
            if sandP1 is None:
                sandP1 = len(sand)
        else:
            for move in [0, -1, 1]:
                newPos = tuple(p + o for p, o in zip(pos, [move, 1]))

                if newPos not in area and newPos not in sand:
                    pastPos.append(pos)
                    pastPos.append(newPos)
                    break

        if len(pastPos) == 0 or pastPos[-1] != newPos:
            sand.add(pos)

    if verbose:
        print(f"\nPart 1:\nUnits of sand that come to rest: {sandP1}\n\nPart 2:\nUnits of sand that come to rest: {len(sand)}")

    return [sandP1, len(sand)]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")