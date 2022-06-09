import time
import re
from itertools import product

class Ingredient:
    def __init__(self, text):
        self.capacity, self.durability, self.flavor, self.texture, self.calories = [int(x) for x in re.findall('-?\d+', text)]

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        ingredients = [Ingredient(line) for line in f.readlines()]

    best = float('-inf')
    best500 = float('-inf')
    for split in product(range(0, 101), repeat=len(ingredients) - 1):
        counts = [split[0]] + [split[i] - split[i - 1] for i in range(1, len(split))] + [100 - split[-1]]
        if min(counts) < 0:
            continue
        
        c = sum(ingredients[i].capacity * counts[i] for i in range(len(ingredients)))
        d = sum(ingredients[i].durability * counts[i] for i in range(len(ingredients)))
        f = sum(ingredients[i].flavor * counts[i] for i in range(len(ingredients)))
        t = sum(ingredients[i].texture * counts[i] for i in range(len(ingredients)))
        cals = sum(ingredients[i].calories * counts[i] for i in range(len(ingredients)))

        if c < 0:
            c = 0
        if d < 0:
            d = 0
        if f < 0:
            f = 0
        if t < 0:
            t = 0

        if c * d * f * t > best:
            best = c * d * f * t

        if cals == 500 and c * d * f * t > best500:
            best500 = c * d * f * t

    print(f"\nPart 1:\nScore of best cookie: {best}")
    print(f"\nPart 2:\nScore of best 500 calorie cookie: {best500}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
