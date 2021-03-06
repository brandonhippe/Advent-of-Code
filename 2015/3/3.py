import time
from collections import defaultdict

DIRS = {'^': (0, 1),'v': (0, -1), '<': (-1, 0), '>': (1, 0)}

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        data = f.readline().strip('\n')

    pos = (0, 0)
    visited = defaultdict(lambda: 0)
    visited[pos] = 1

    for d in data:
        pos = tuple(p + o for p, o in zip(pos, DIRS[d]))
        visited[pos] += 1

    print(f"\nPart 1:\nNumber of houses that receive at least 1 present: {len(visited)}")

    pos = [(0, 0), (0, 0)]
    visited = defaultdict(lambda: 0)
    visited[pos[0]] = 2

    for i in range(0, len(data), 2):
        for n in range(2):
            pos[n] = tuple(p + o for p, o in zip(pos[n], DIRS[data[i + n]]))
            visited[pos[n]] += 1

    print(f"\nPart 2:\nNumber of houses that receive at least 1 present: {len(visited)}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
