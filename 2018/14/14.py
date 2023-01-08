import time

def main(verbose):
    recipes = '380621'
    scores = '37'    
    elfIndexes = [0, 1]

    p1 = False
    p2 = False
    while not p1 or not p2:
        scores += str(int(scores[elfIndexes[0]]) + int(scores[elfIndexes[1]]))

        if not p2 and recipes in scores[-1 - len(recipes):]:
            p2 = True

        for i in range(2):
            elfIndexes[i] += int(scores[elfIndexes[i]]) + 1
            elfIndexes[i] %= len(scores)

        if not p1 and len(scores) >= int(recipes) + 10:
            part1 = int(scores[int(recipes): int(recipes) + 11])
            p1 = True

    part2 = scores.index(recipes)

    if verbose:
        print(f"\nPart 1:\nNext 10 scores: {part1}\n\nPart 2: First occurance of {recipes}: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
