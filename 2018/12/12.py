import time
from collections import defaultdict

def iterate(plantState, rules):
    newPlantState = defaultdict(lambda: '.')

    for i in range(min(plantState.keys()) - 2, max(plantState.keys()) + 3):
        plantString = ''.join(plantState[i + c] for c in range(-2, 3))
        if plantString in rules:
            newPlantState[i] = '#'

    return newPlantState

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    plantState = defaultdict(lambda: '.')
    for i, c in enumerate(lines[0].split(": ")[1]):
        plantState[i] = c

    rules = {line.split(" => ")[0] for line in lines[2:] if line.split(" => ")[1] == '#'}

    gen = 0
    genData = [sum(k for k, v in zip(plantState.keys(), plantState.values()) if v == '#')]
    deltas = []
    while True:
        gen += 1
        plantState = iterate(plantState, rules)
        totalPlants = sum(k for k, v in zip(plantState.keys(), plantState.values()) if v == '#')
        genData.append(totalPlants)
        deltas.append(genData[gen] - genData[gen - 1])

        if gen == 20:
            print(f"\nPart 1:\nSum of all numbers of pots that contain plants after 20 generations: {totalPlants}")

        if gen >= 20 and len(set(deltas[-10:])) == 1:
            break

    print(f"\nPart 2:\nSum of all numbers of pots that contain plants after 50,000,000,000 generations: {totalPlants + ((50000000000 - gen) * deltas[-1])}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
