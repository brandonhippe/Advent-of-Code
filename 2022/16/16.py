from time import perf_counter
import re, sys
from collections import defaultdict
sys.path.insert(0,"C:/Users/Brandon Hippe/Documents/Coding Projects/Advent-of-Code/Modules")
from progressbar import printProgressBar


def dfs(currValve, flowRates, connections, valveBits, openValves, timeRem, memo):
    if timeRem <= 1:
        memo[(currValve, openValves, timeRem)] = 0
        return 0

    if (currValve, openValves, timeRem) in memo:
        return memo[(currValve, openValves, timeRem)]

    openValves |= 1 << valveBits[currValve]
    released = timeRem * flowRates[currValve]

    maxReleased = 0
    for v, t in zip(connections[currValve].keys(), connections[currValve].values()):
        if openValves & 1 << valveBits[v] == 1 << valveBits[v]:
            continue
        
        if (v, openValves, timeRem - t) not in memo:
            dfs(v, flowRates, connections, valveBits, openValves, timeRem - t, memo)
        
        maxReleased = max(maxReleased, memo[(v, openValves, timeRem - t)])

    openValves &= ~(1 << valveBits[currValve])

    memo[(currValve, openValves, timeRem)] = released + maxReleased
    return released + maxReleased


def floydWarshall(connections):
    for k in connections.keys():
        connections[k][k] = 0

    for k in connections.keys():
        for i in connections.keys():
            for j in connections.keys():
                connections[i][j] = min(connections[i][j], connections[i][k] + connections[k][j])

    return connections


def main(verbose):
    with open("input.txt", encoding="UTF-8") as f:
        lines = [line.strip('\n') for line in f.readlines()]

    flowRates = {}
    connections = {}

    for line in lines:
        splitLine = line.split(" ")
        flowRates[splitLine[1]] = [int(x) for x in re.findall("\d+", line)][0]
        connections[splitLine[1]] = defaultdict(lambda: float('inf'))
        for v in splitLine[9:]:
            connections[splitLine[1]][v.strip(',')] = 1

    connections = floydWarshall(connections)

    unimportant = [v for v in flowRates.keys() if flowRates[v] == 0 and v != 'AA']

    for v in unimportant:
        for k in connections.keys():
            del(connections[k][v])

        del(flowRates[v])
        del(connections[v])

    valveBits = {'AA': 0}
    bit = 1
    for k in connections.keys():
        if k != 'AA':
            valveBits[k] = bit
            bit += 1

        for k1 in list(connections[k].keys()):
            if k1 == k:
                del(connections[k][k1])
            else:
                connections[k][k1] += 1

    memo = {}
    pressure = dfs('AA', flowRates, connections, valveBits, 0, 30, memo)
 

    maxPressure = pressure
    for i in range(2 ** (len(flowRates) - 1)):
        if verbose:
            printProgressBar(i + 1, 2 ** (len(flowRates) - 1))
        maxPressure = max(maxPressure, dfs('AA', flowRates, connections, valveBits, i << 1, 26, memo) + dfs('AA', flowRates, connections, valveBits, (~i) << 1, 26, memo))

    if verbose:
        print(f"\nPart 1:\n{pressure}\n\nPart 2:\n{maxPressure}")

    return [pressure, maxPressure]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")