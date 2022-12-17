from time import perf_counter
import re
from collections import defaultdict


def dfs(currValve, flowRates, connections, validValves, openValves, timeRem):
    if timeRem <= 1:
        return 0

    openValves.add(currValve)
    released = timeRem * flowRates[currValve]

    maxReleased = 0
    for v, t in zip(connections[currValve].keys(), connections[currValve].values()):
        if v in openValves or v not in validValves:
            continue

        maxReleased = max(maxReleased, dfs(v, flowRates, connections, validValves, openValves, timeRem - t))

    openValves.remove(currValve)

    return released + maxReleased


def main(filename):
    with open(filename, encoding="UTF-8") as f:
        lines = [line.strip('\n') for line in f.readlines()]

    flowRates = {}
    connections = {}

    for line in lines:
        splitLine = line.split(" ")
        flowRates[splitLine[1]] = [int(x) for x in re.findall("\d+", line)][0]
        connections[splitLine[1]] = defaultdict(lambda: float('inf'))
        for v in splitLine[9:]:
            connections[splitLine[1]][v.strip(',')] = 1

    for k in connections.keys():
        connections[k][k] = 0

    for k in connections.keys():
        for i in connections.keys():
            for j in connections.keys():
                connections[i][j] = min(connections[i][j], connections[i][k] + connections[k][j])

    unimportant = [v for v in flowRates.keys() if flowRates[v] == 0 and v != 'AA']

    for v in unimportant:
        for k in connections.keys():
            del(connections[k][v])

        del(flowRates[v])
        del(connections[v])

    for k in connections.keys():
        for k1 in list(connections[k].keys()):
            if k1 == k:
                del(connections[k][k1])
            else:
                connections[k][k1] += 1

    pressure = dfs('AA', flowRates, connections, set(flowRates.keys()), set(), 30)
 
    print(f"\nPart 1:\n{pressure}")

    maxPressure = pressure
    for i in range(2 ** (len(flowRates) - 1)):
        print(f"{i + 1}/{2 ** (len(flowRates) - 1)}")
        validValves = [set(), set()]
        b = bin(i)[2:]
        b += '0' * (len(flowRates) - 1 - len(b))

        for i, v in enumerate([valve for valve in flowRates.keys() if valve != 'AA']):
            validValves[int(b[i])].add(v)

        maxPressure = max(maxPressure, sum(dfs('AA', flowRates, connections, valid, set(), 26) for valid in validValves))


    print(f"\nPart 2:\n{maxPressure}")


if __name__ == "__main__":
    init_time = perf_counter()
    main("input.txt")
    print(f"\nRan in {perf_counter() - init_time} seconds.")