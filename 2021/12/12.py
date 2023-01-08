import time
from collections import defaultdict


def findPaths(curr, caves, visited, p2):
    if curr == "end":
        return 1

    if curr.islower():
        visited[curr] += 1

    paths = 0
    for n in list(caves[curr]):
        if n == "start":
            continue

        if visited[n] == 0 or (p2 and max(visited.values()) == 1):
            paths += findPaths(n, caves, visited, p2)

    if curr.islower():
        visited[curr] -= 1

    return paths


def main(verbose):
    with open('input.txt', encoding='UTF-8') as f:
        lines = [line.strip() for line in f.readlines()]

    caves = defaultdict(lambda: set())
    for line in lines:
        line = line.split('-')
        
        caves[line[0]].add(line[1])
        caves[line[1]].add(line[0])

    part1 = findPaths('start', caves, defaultdict(lambda: 0), False)
    part2 = findPaths('start', caves, defaultdict(lambda: 0), True)

    if verbose:
        print(f"\nPart 1:\nNumber of paths visiting small caves once: {part1}\n\nPart 2:\nNumber of paths visiting small caves once: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds")
