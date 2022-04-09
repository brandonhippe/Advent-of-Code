import time

def main(recipes: str ='380621'):
    # 380621 is puzzle input
    scores = '37'    
    elfIndexes = [0, 1]

    part1 = False
    part2 = False
    while not part1 or not part2:
        scores += str(int(scores[elfIndexes[0]]) + int(scores[elfIndexes[1]]))

        if not part2 and recipes in scores[-1 - len(recipes):]:
            part2 = True

        for i in range(2):
            elfIndexes[i] += int(scores[elfIndexes[i]]) + 1
            elfIndexes[i] %= len(scores)

        if not part1 and len(scores) >= int(recipes) + 10:
            print(f"\nPart 1:\nNext 10 scores: {scores[int(recipes): int(recipes) + 11]}")
            part1 = True

    print(f"\nPart 2: First occurance of {recipes}: {scores.index(recipes)}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main()
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
