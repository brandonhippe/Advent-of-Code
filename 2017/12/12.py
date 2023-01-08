import time
import re

class Program:
    def __init__(self, pNum):
        self.pNum = pNum
        self.pipes = set()

def bfs(start, visited):
    openList = [start]

    while len(openList) != 0:
        p = openList.pop(0)
        for s in p.pipes:
            if not visited[s.pNum]:
                openList.append(s)

        visited[p.pNum] = True

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    programs = [Program(i) for i in range(len(lines))]

    for i, line in enumerate(lines):
        ps = [int(x) for x in re.findall('\d+', line.split('> ')[1])]
        for p in ps:
            programs[i].pipes.add(programs[p])
            programs[p].pipes.add(programs[i])

    visited = [False] * len(programs)
    bfs(programs[0], visited)

    part1 = sum(visited)

    groups = 1
    for i, v in enumerate(visited):
        if not v:
            bfs(programs[i], visited)
            groups += 1

    if verbose:
        print(f"\nPart 1:\nPrograms connected to program 0: {part1}\n\nPart 2:\nNumber of groups: {groups}")

    return [part1, groups]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
