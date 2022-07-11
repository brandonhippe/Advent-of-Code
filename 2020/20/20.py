import time
import re
import numpy as np
from collections import defaultdict

def transform(input_img, amt):
    output_img = np.rot90(input_img, amt)
    if amt >= 4:
        output_img = np.flipud(output_img)

    return output_img

def assembleImage(corner, tiles, sideInfo, sideMatches):
    line = tiles[corner][1:-1, 1:-1]

    curr = corner
    while ''.join(tiles[curr][:, -1]) in sideInfo:
        rightSide = ''.join(tiles[curr][:, -1])
        curr = list(sideInfo[rightSide].intersection(sideMatches[curr]))[0]

        r = 0
        while ''.join(transform(tiles[curr], r)[:, 0]) != rightSide:
            r += 1

        tiles[curr] = transform(tiles[curr], r)

        line = np.concatenate([line, tiles[curr][1:-1, 1:-1]], axis=1)

    bottomSide = ''.join(tiles[corner][-1, :])
    if bottomSide in sideInfo:
        newCorner = list(sideInfo[bottomSide].intersection(sideMatches[corner]))[0]

        r = 0
        while ''.join(transform(tiles[newCorner], r)[0, :]) != bottomSide:
            r += 1

        tiles[newCorner] = transform(tiles[newCorner], r)

        return np.concatenate([line, assembleImage(newCorner, tiles, sideInfo, sideMatches)], axis=0)
    else:
        return line

def getRoughness(image, monster):
    monsters = 0
    water = {(i, j) for i in range(len(image[0])) for j in range(len(image)) if image[j, i] == '#'}

    for y in range(len(image) - len(monster)):
        for x in range(len(image[y]) - len(monster[0])):
            if all(image[y + j, x + i] == monster[j, i] if monster[j, i] == '#' else True for i in range(len(monster[0])) for j in range(len(monster))):
                monsters += 1
                for j in range(len(monster)):
                    for i in range(len(monster[j])):
                        if monster[j, i] == '#' and (x + i, y + j) in water:
                            water.remove((x + i, y + j))

    return (monsters, len(water))

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        data = '\n'.join(line.strip('\n') for line in f.readlines() if len(line.strip('\n')) != 0)

    tiles = {num: tile for num, tile in zip([int(x) for x in re.findall('\d+', data)], [np.asarray([list(l) for l in line.strip('\n').split('\n')]) for line in re.split('Tile \d+:', data)[1:]])}
    sideInfo = defaultdict(lambda: set())

    for n, t in zip(tiles.keys(), tiles.values()):
        for i in range(4):
            sideInfo[''.join(np.rot90(t, i)[-1, :])].add(n)
            sideInfo[''.join(np.rot90(t, i)[-1, ::-1])].add(n)

    sideMatches = defaultdict(lambda: set())

    for side, s in zip(list(sideInfo.keys()), list(sideInfo.values())):
        if len(s) == 1:
            del sideInfo[side]
        else:
            for id in list(s):
                sideMatches[id] = sideMatches[id].union(s)
                sideMatches[id].remove(id)

    prod = 1
    corner = None
    for n, s in zip(sideMatches.keys(), sideMatches.values()):
        if len(s) == 2:
            prod *= n

            if corner is None:
                corner = n
                r = 0
                while ''.join(transform(tiles[corner], r)[-1, :]) not in sideInfo or ''.join(transform(tiles[corner], r)[:, -1]) not in sideInfo:
                    r += 1

                tiles[corner] = transform(tiles[corner], r)

    print(f"\nPart 1:\nProduct of Corner image IDs: {prod}")

    image = assembleImage(corner, tiles, sideInfo, sideMatches)

    with open("monster.txt", encoding='UTF-8') as f:
        monster = np.asarray([list(l.strip('\n')) for l in f.readlines()])

    r = 0
    monsters = 0
    while monsters == 0:
        monsters, roughness = getRoughness(transform(image, r), monster)
        r += 1

    print(f"\nPart 2:\nWater Roughness: {roughness}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
