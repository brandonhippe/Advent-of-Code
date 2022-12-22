from time import perf_counter
import re
from math import ceil
from collections import defaultdict


def bfs(oreCost, clayOre, obsOre, obsClay, geoOre, geoObs, maxT):
    states = defaultdict(set)
    states[0].add((0, 0, 0, 0, 1, 0, 0))

    maxGeodes = 0
    while sum(len(states[k]) for k in states.keys()) != 0:
        minK = min(list(states.keys()))

        for state in list(states[minK]):
            geodes, ore, clay, obs, oreR, clayR, obsR = state

            maxGeodes = max(maxGeodes, geodes)

            ## Save up to make Geode Robot
            if obsR != 0:
                timeTaken = ceil(max((geoOre - ore) / oreR, (geoObs - obs) / obsR)) + 1

                if timeTaken <= maxT - minK and timeTaken > 0:
                    states[minK + timeTaken].add((geodes + maxT - (minK + timeTaken), ore + (oreR * timeTaken) - geoOre, clay + (clayR * timeTaken), obs + (obsR * timeTaken) - geoObs, oreR, clayR, obsR))

            ## Save up to make Obsidian Robot
            if clayR != 0 and obsR < geoObs and timeTaken > 0:
                timeTaken = ceil(max((obsOre - ore) / oreR, (obsClay - clay) / clayR)) + 1

                if timeTaken <= maxT - minK and timeTaken > 0:
                    states[minK + timeTaken].add((geodes, ore + (oreR * timeTaken) - obsOre, clay + (clayR * timeTaken) - obsClay, obs + (obsR * timeTaken), oreR, clayR, obsR + 1))


            ## Save up to make Clay Robot
            if clayR < obsClay:
                timeTaken = ceil((clayOre - ore) / oreR) + 1

                if timeTaken <= maxT - minK and timeTaken > 0:
                    states[minK + timeTaken].add((geodes, ore + (oreR * timeTaken) - clayOre, clay + (clayR * timeTaken), obs + (obsR * timeTaken), oreR, clayR + 1, obsR))


            ## Save up to make Ore Robot
            if oreR < max(clayOre, obsOre, geoOre):
                timeTaken = ceil((oreCost - ore) / oreR) + 1

                if timeTaken <= maxT - minK and timeTaken > 0:
                    states[minK + timeTaken].add((geodes, ore + (oreR * timeTaken) - oreCost, clay + (clayR * timeTaken), obs + (obsR * timeTaken), oreR + 1, clayR, obsR))

            states[minK].remove(state)

        if len(states[minK]) == 0:
            del(states[minK])

    return maxGeodes



def mostGeodes(oreCost, clayOre, obsOre, obsClay, geoOre, geoObs, maxT):
    states = {(0, 0, 0, 0, 1, 0, 0)}

    maxGeodes = 0
    for t in range(maxT):
        newStates = set()

        for state in states:
            ore, clay, obs, geo, oreR, clayR, obsR = state
            newOre = ore + oreR
            newClay = clay + clayR
            newObs = obs + obsR

            maxGeodes = max(maxGeodes, geo)

            if ore >= geoOre and obs >= geoObs:
                newStates.add((newOre - geoOre, newClay, newObs - geoObs, geo + maxT - t - 1, oreR, clayR, obsR))
            else:
                newStates.add((newOre, newClay, newObs, geo, oreR, clayR, obsR))

                if ore >= oreCost and oreR <= max(clayOre, obsOre, geoOre):
                    newStates.add((newOre - oreCost, newClay, newObs, geo, oreR + 1, clayR, obsR))

                if ore >= clayOre and clayR <= obsClay:
                    newStates.add((newOre - clayOre, newClay, newObs, geo, oreR, clayR + 1, obsR))

                if ore >= obsOre and clay >= obsClay and obsR <= geoObs:
                    newStates.add((newOre - obsOre, newClay - obsClay, newObs, geo, oreR, clayR, obsR + 1))


        states = set()
        if t == maxT - 1:
            break

        for state in newStates:
            if state[3] + maxT - 1 - t >= maxGeodes:
                states.add(state)

    return maxGeodes


def main(filename):
    with open(filename, encoding="UTF-8") as f:
        lines = [line.strip('\n') for line in f.readlines()]

    qualitySum = 0
    for line in lines:
        blueprint, oreCost, clayOre, obsOre, obsClay, geoOre, geoObs = [int(x) for x in re.findall('\d+', line)]
        qualitySum += blueprint * bfs(oreCost, clayOre, obsOre, obsClay, geoOre, geoObs, 24)
 
    print(f"\nPart 1:\n{qualitySum}")

    product = 1
    for line in lines[:3]:
        blueprint, oreCost, clayOre, obsOre, obsClay, geoOre, geoObs = [int(x) for x in re.findall('\d+', line)]
        product *= mostGeodes(oreCost, clayOre, obsOre, obsClay, geoOre, geoObs, 32)

    print(f"\nPart 2:\n{product}")


if __name__ == "__main__":
    init_time = perf_counter()
    main("input.txt")
    print(f"\nRan in {perf_counter() - init_time} seconds.")