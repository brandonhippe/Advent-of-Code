import time

MOVES = {'n': (0, -1), 'ne': (1, -1), 'se': (1, 0), 's': (0, 1), 'sw': (-1, 1), 'nw': (-1, 0)}

def manhatDist(p1, p2):
    return sum([abs(c1 - c2) for c1, c2 in zip(p1, p2)])

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        steps = f.readline().strip('\n').split(',')

    pos = (0, 0)

    farthest = 0
    for step in steps:
        pos = tuple(p + o for p, o in zip(pos, MOVES[step]))

        d = manhatDist((*pos, -pos[0] - pos[1]), (0, 0, 0)) // 2
        if d > farthest:
            farthest = d

    print(f"\nPart 1:\nFewest steps to child process: {d}")
    print(f"\nPart 2:\nFarthest ever reached: {farthest}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
