import time
import re

def manhatDist(p1, p2):
    return sum([abs(c1 - c2) for c1, c2 in zip(p1, p2)])

def main(filename):
    with open(filename, encoding='UTF-8') as f:
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

    print(f"\nPart 1:\nDistance to Easter Bunny HQ: {manhatDist(pos, [0] * len(pos))}")
    print(f"\nPart 2:\nDistance to first repeated position: {manhatDist(firstRepeat, [0] * len(firstRepeat))}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
