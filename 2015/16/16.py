import time
import re

class Sue:
    def __init__(self, text):
        self.characteristics = set(re.split(', ', re.split(': ', text, 1)[1]))

def gt(a, b):
    return a > b

def lt(a, b):
    return a < b

def eq(a, b):
    return a == b

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        data = [Sue(line.strip('\n')) for line in f.readlines()]

    identifiers = {"children: 3", "cats: 7", "samoyeds: 2", "pomeranians: 3", "akitas: 0", "vizslas: 0", "goldfish: 5", "trees: 3", "cars: 2", "perfumes: 1"}
    possible = []
    for i, s in enumerate(data):
        if len(identifiers.union(s.characteristics)) == len(identifiers):
            possible.append(i + 1)

    print(f"\nPart 1:\nPossible Susans: {possible}")
    
    identifiers = {"children": [eq, 3], "cats": [gt, 7], "samoyeds": [eq, 2], "pomeranians": [lt, 3], "akitas": [eq, 0], "vizslas": [eq, 0], "goldfish": [lt, 5], "trees": [gt, 3], "cars": [eq, 2], "perfumes": [eq, 1]}
    possible = []
    for i, s in enumerate(data):
        s.characteristics = {c.split(':')[0]: int(c.split(' ')[1]) for c in s.characteristics}
        
        valid = True
        for k, v in zip(s.characteristics.keys(), s.characteristics.values()):
            if not identifiers[k][0](v, identifiers[k][1]):
                valid = False
                break

        if valid:
            possible.append(i + 1)

    print(f"\nPart 2:\nPossible Susans: {possible}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
