from time import perf_counter
import re

def main(filename):
    with open(filename, encoding="UTF-8") as f:
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

    sand = set()
    settled = True
    while settled:
        settled = False

        pos = (500, 0)

        dropped = True
        while dropped:
            dropped = False

            for move in [0, -1, 1]:
                newPos = tuple(p + o for p, o in zip(pos, [move, 1]))

                if newPos[1] == maxY:
                    pos = newPos
                    break

                if newPos not in area and newPos not in sand:
                    dropped = True
                    pos = newPos
                    break

            if not dropped:
                settled = pos[1] != maxY

        if settled:
            sand.add(pos)


    print(f"\nPart 1:\nUnits of sand that come to rest: {len(sand)}")

    sand = set()
    while (500, 0) not in sand:
        pos = (500, 0)

        dropped = True
        while dropped and pos[1] != maxY:
            dropped = False

            for move in [0, -1, 1]:
                newPos = tuple(p + o for p, o in zip(pos, [move, 1]))

                if newPos not in area and newPos not in sand:
                    dropped = True
                    pos = newPos
                    break

        sand.add(pos)

    print(f"\nPart 2:\nUnits of sand that come to rest: {len(sand)}")


if __name__ == "__main__":
    init_time = perf_counter()
    main("input.txt")
    print(f"\nRan in {perf_counter() - init_time} seconds.")