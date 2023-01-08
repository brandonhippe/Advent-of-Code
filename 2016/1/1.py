import time
import re

def manhatDist(p1, p2):
    return sum([abs(c1 - c2) for c1, c2 in zip(p1, p2)])

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        data = f.readline().split(',')

    pos = (0, 0)
    facing = (0, -1)
    visited = {pos}
    firstRepeat = None

    for d in data:
        if 'L' in d:
            facing = (facing[1], -facing[0])
        else:
            facing = (-facing[1], facing[0])

        for _ in range(int(re.findall('\d+', d)[0])):
            pos = tuple(p + o for p, o in zip(pos, facing))

            if pos in visited and firstRepeat is None:
                firstRepeat = pos

            visited.add(pos)

    part1 = manhatDist(pos, [0] * len(pos))
    part2 = manhatDist(firstRepeat, [0] * len(firstRepeat))

    if verbose:
        print(f"\nPart 1:\nDistance to Easter Bunny HQ: {part1}\n\nPart 2:\nDistance to first repeated position: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
