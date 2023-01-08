import time
from collections import defaultdict

def manhatDist(p1, p2):
    return sum([abs(c1 - c2) for c1, c2 in zip(p1, p2)])

def sqIndexPos(sq):
    odd = 1
    while odd * odd <= sq:
        odd += 2

    odd -= 2
    pos = [odd // 2] * 2
    ix = odd * odd

    if ix == sq:
        return pos

    pos[0] += 1
    ix += 1
    dirs = [[[0, -1], odd], [[-1, 0], odd + 1], [[0, 1], odd + 1], [[1, 0], odd + 1]]
    while sq - ix > dirs[0][-1]:
        offset, d = dirs.pop(0)
        ix += d
        pos = [p + (d * o) for p, o in zip(pos, offset)]

    offset, d = dirs[0]

    return [p + ((sq - ix) * o) for p, o in zip(pos, offset)]

def main(verbose):
    data = 325489
    part1 = manhatDist(sqIndexPos(data), (0, 0))

    generated = defaultdict(lambda: 0)
    generated[(0, 0)] = 1
    lastGenerated = 1
    pos = [1, 0]
    dirs = [[[0, -1], 1], [[-1, 0], 2], [[0, 1], 2], [[1, 0], 3]]
    
    while lastGenerated < data:
        offset, d = dirs.pop(0)

        for _ in range(d):
            lastGenerated = sum([generated[tuple(p + o for p, o in zip(pos, off))] for off in [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]])
            if lastGenerated > data:
                break

            generated[tuple(pos)] = lastGenerated

            pos = [p + o for p, o in zip(pos, offset)]

        dirs.append([offset, d + 2])

    if verbose:
        print(f"\nPart 1:\nSteps to access port: {part1}\n\nPart 2:\nFirst value written larger than input: {lastGenerated}")

    return [part1, lastGenerated]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
