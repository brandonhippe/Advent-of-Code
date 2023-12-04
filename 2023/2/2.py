from time import perf_counter
import re
from collections import defaultdict


COLORS = {'blue': 14, 'green': 13, 'red': 12}

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    part1 = 0
    gameData = []
    for line in lines:
        gameData.append(defaultdict(lambda: 0))
        id = int(re.findall('\d+', line)[0])

        data = line.split(": ")[1]
        validId = True
        for draw in data.split("; "):
            for color_data in draw.split(', '):
                n, c = color_data.split(' ')

                if int(n) > COLORS[c]:
                    validId = False

                gameData[-1][c] = max(gameData[-1][c], int(n))

        if validId:
            part1 += id

    part2 = 0
    for game in gameData:
        p = 1
        for n in game.values():
            p *= n

        part2 += p

    if verbose:
        print(f"\nPart 1:\nSum of IDs of possible games: {part1}\n\nPart 2:\nSum of power sets of games: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")
