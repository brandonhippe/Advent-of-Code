import time
import re
from collections import defaultdict

def removePossible(allergen, possible):
    if len(possible[allergen]) != 1:
        return

    possible[allergen] = list(possible[allergen])[0]
    for a in possible.keys():
        if a == allergen:
            continue

        if possible[allergen] in possible[a]:
            possible[a].remove(possible[allergen])
            removePossible(a, possible)

    return

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        data = [line.strip(')\n') for line in f.readlines()]

    ingredients = defaultdict(lambda: set())
    ingredientOccurrances = defaultdict(lambda: 0)
    allergens = defaultdict(lambda: set())
    
    for i, line in enumerate(data):
        line = line.replace(',', '')
        ings, alls = re.split(' \(contains ', line)
        for ingredient in re.split(' ', ings):
            ingredients[ingredient].add(i)
            ingredientOccurrances[ingredient] += 1

        for allergen in re.split(' ', alls):
            allergens[allergen].add(i)

    possible = {a: set(ingredients.keys()) for a in allergens.keys()}

    for a in allergens.keys():
        for i in list(possible[a]):
            if ingredients[i].union(allergens[a]) != ingredients[i]:
                possible[a].remove(i)
                removePossible(a, possible)

    print(f"\nPart 1:\nNumber of occurrances of ingredients that aren't allergens: {sum([v for k, v in zip(ingredientOccurrances.keys(), ingredientOccurrances.values()) if k not in possible.values()])}")
    print(f"\nPart 2:\nCanonical dangerous ingredient list:\n{','.join(e[1] for e in sorted(zip(possible.keys(), possible.values()), key=lambda e: e[0]))}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
