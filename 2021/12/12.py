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


def main():
    with open('input.txt', encoding='UTF-8') as f:
        lines = [line.strip() for line in f.readlines()]

    caves = defaultdict(lambda: set())
    for line in lines:
        line = line.split('-')
        
        caves[line[0]].add(line[1])
        caves[line[1]].add(line[0])

    print(f"\nPart 1:\nNumber of paths visiting small caves once: {findPaths('start', caves, defaultdict(lambda: 0), False)}")
    print(f"\nPart 2:\nNumber of paths visiting small caves once: {findPaths('start', caves, defaultdict(lambda: 0), True)}")

init_time = time.perf_counter()
main()
print(f"\nRan in {time.perf_counter() - init_time} seconds")
