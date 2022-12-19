from time import perf_counter
import re, sys
sys.path.insert(0,"C:/Users/Brandon Hippe/Documents/Coding Projects/Advent-of-Code/Modules")
from progressbar import printProgressBar


def mostGeodes(oreCost, clayOre, obsOre, obsClay, geoOre, geoObs, maxT):
    states = {(0, 0, 0, 0, 1, 0, 0, 0)}

    maxGeodes = 0
    for t in range(maxT):
        printProgressBar(t + 1, maxT)
        newStates = set()

        for state in states:
            ore, clay, obs, geo, oreR, clayR, obsR, geoR = state
            newOre = ore + oreR
            newClay = clay + clayR
            newObs = obs + obsR
            newGeo = geo + geoR

            maxGeodes = max(maxGeodes, newGeo)

            newStates.add((newOre, newClay, newObs, newGeo, oreR, clayR, obsR, geoR))

            if ore >= oreCost and oreR <= max(oreCost, clayOre, obsOre, geoOre):
                newStates.add((newOre - oreCost, newClay, newObs, newGeo, oreR + 1, clayR, obsR, geoR))

            if ore >= clayOre and clayR <= obsClay:
                newStates.add((newOre - clayOre, newClay, newObs, newGeo, oreR, clayR + 1, obsR, geoR))

            if ore >= obsOre and clay >= obsClay and obsR <= geoObs:
                newStates.add((newOre - obsOre, newClay - obsClay, newObs, newGeo, oreR, clayR, obsR + 1, geoR))

            if ore >= geoOre and obs >= geoObs:
                newStates.add((newOre - geoOre, newClay, newObs - geoObs, newGeo, oreR, clayR, obsR, geoR + 1))

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
        
        geodes = mostGeodes(oreCost, clayOre, obsOre, obsClay, geoOre, geoObs, 24)
        print(f"{blueprint = }: {geodes = }")
        qualitySum += blueprint * geodes
 
    print(f"\nPart 1:\n{qualitySum}")

    product = 1
    for line in lines[:3]:
        blueprint, oreCost, clayOre, obsOre, obsClay, geoOre, geoObs = [int(x) for x in re.findall('\d+', line)]

        geodes = mostGeodes(oreCost, clayOre, obsOre, obsClay, geoOre, geoObs, 32)
        print(f"{blueprint = }: {geodes = }")
        product *= geodes

    print(f"\nPart 2:\n{product}")


if __name__ == "__main__":
    init_time = perf_counter()
    main("input.txt")
    print(f"\nRan in {perf_counter() - init_time} seconds.")