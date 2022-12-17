from time import perf_counter
import re
from collections import defaultdict


def dfs(currValve, flowRates, connections, openValves, timeRem):
    if timeRem <= 1:
        return 0

    openValves.add(currValve)
    released = timeRem * flowRates[currValve]

    maxReleased = 0
    for v, t in zip(connections[currValve].keys(), connections[currValve].values()):
        if v in openValves:
            continue

        maxReleased = max(maxReleased, dfs(v, flowRates, connections, openValves, timeRem - t))

    openValves.remove(currValve)

    return released + maxReleased


def dfsPath(currValve, connections, openValves, timeRem):
    if timeRem <= 1:
        return [None]

    openValves.add(currValve)
    paths = []
    for v, t in zip(connections[currValve].keys(), connections[currValve].values()):
        if v in openValves:
            continue

        for p in dfsPath(v, connections, openValves, timeRem - t):
            if p is None:
                paths.append([v])
            else:
                paths.append([v] + p)

    openValves.remove(currValve)

    return paths


def elephantDfs(currValves, moveTimes, flowRates, connections, openValves, timeRem):
    subTime = min(moveTimes)
    moveTimes = [m - subTime for m in moveTimes]
    timeRem -= subTime

    ix = moveTimes.index(0)
    released = timeRem * flowRates[currValves[ix]]

    maxReleased = 0
    for v, t in zip(connections[currValves[ix]].keys(), connections[currValves[ix]].values()):
        if v in openValves or t >= timeRem:
            continue

        if ix == 0:
            newValves = [v, currValves[1]]
            newTimes = [t, moveTimes[1]]
        else:
            newValves = [currValves[0], v]
            newTimes = [moveTimes[0], t]
        
        openValves.add(v)
        maxReleased = max(maxReleased, elephantDfs(newValves, newTimes, flowRates, connections, openValves, timeRem))
        openValves.remove(v)

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

    pressure = dfs('AA', flowRates, connections, set(), 30)
 
    print(f"\nPart 1:\n{pressure}")

    maxPressure = pressure
    count = 0
    for i, humanStart in enumerate(list(connections['AA'].keys())[:-1]):
        for elephantStart in list(connections['AA'].keys())[i + 1:]:
            if {humanStart, elephantStart} == {'JJ', 'DD'}:
                print("Check")
            print(f"{count + 1}/{len(connections['AA']) * (len(connections['AA']) - 1) // 2}")
            count += 1
            maxPressure = max(maxPressure, elephantDfs([humanStart, elephantStart], [connections['AA'][humanStart], connections['AA'][elephantStart]], flowRates, connections, {'AA', humanStart, elephantStart}, 26))

    print(f"\nPart 2:\n{maxPressure}")


if __name__ == "__main__":
    init_time = perf_counter()
    main("input1.txt")
    print(f"\nRan in {perf_counter() - init_time} seconds.")