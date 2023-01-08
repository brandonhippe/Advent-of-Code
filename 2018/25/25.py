import time
import re

def manhatDist(p1, p2):
    d = sum([abs(c2 - c1) for c1, c2 in zip(p1, p2)])
    return d

def scc(points, neighbors):
    visited = set()
    components = []

    for p in points:
        if p in visited:
            continue
        
        components.append([])
        openList = [p]

        while len(openList) != 0:
            currP = openList.pop(0)
            components[-1].append(currP)
            
            for n in neighbors[currP]:
                if n not in visited:
                    openList.append(n)

            visited.add(currP)

    return components

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        points = [tuple(int(x) for x in re.findall('-?\d+', line)) for line in f.readlines()]

    neighbors = {p: [p1 for p1 in points if p != p1 and manhatDist(p, p1) <= 3] for p in points}
    part1 = len(scc(points, neighbors))

    if verbose:
        print(f"\nPart 1:\nNumber of constellations: {part1}")

    return [part1]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
