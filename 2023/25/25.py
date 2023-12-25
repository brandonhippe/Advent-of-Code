from time import perf_counter
from collections import defaultdict
from itertools import product
from copy import deepcopy
import random


def kargers(connections, connectionSet):
    cg = deepcopy(connections)
    cgSet = deepcopy(connectionSet)

    while len(cg) != 2:
        c = random.choice(list(cgSet))
        cgSet.remove(c)
        v1, v2 = c
        newV = v1 + v2
        cg[newV] = set()
        for n1 in cg[v1]:
            if n1 == v2:
                continue

            cg[n1].remove(v1)
            cgSet.remove(tuple(sorted([n1, v1])))
            cgSet.add(tuple(sorted([n1, newV])))
            cg[newV].add(n1)
            cg[n1].add(newV)

        for n2 in cg[v2]:
            if n2 == v1:
                continue

            cg[n2].remove(v2)
            cgSet.remove(tuple(sorted([n2, v2])))
            cgSet.add(tuple(sorted([n2, newV])))
            cg[newV].add(n2)
            cg[n2].add(newV)


        del(cg[v1], cg[v2])

    return cg


def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    connections = defaultdict(lambda: set())
    connectionSet = set()
    for line in lines:
        name, conns = line.split(": ")
        for c in conns.split(' '):
            connections[name].add(c)
            connections[c].add(name)
            connectionSet.add(tuple(sorted([name, c])))

    while True:
        testSet = deepcopy(connectionSet)
        groups = [[k[i:i + 3] for i in range(0, len(k), 3)] for k in kargers(connections, connectionSet).keys()]

        for i in range(len(groups)):
            for n1, n2 in product(groups[i], repeat = 2):
                conn = tuple(sorted([n1, n2]))
                if conn in testSet:
                    testSet.remove(conn)

        if len(testSet) == 3:
            break        

    part1 = len(groups[0]) * len(groups[1])
    part2 = 0

    if verbose:
        print(f"\nPart 1:\nProduct of disconnected group sizes{part1}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")
