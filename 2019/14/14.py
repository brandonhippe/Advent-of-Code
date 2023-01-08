import math
import time

class reaction:
    def __init__(self, line):
        line = line.split(' => ')
        for (i, l) in enumerate(line):
            line[i] = l.split(',')

        self.inputs = {}
        self.outputs = {}

        for inp in line[0]:
            inp = inp.strip()
            inp = inp.split(' ')
            self.inputs[inp[1]] = int(inp[0])

        for out in line[1]:
            out = out.split(' ')
            self.outputs[out[1]] = int(out[0])

def oreNeeded(chemicals, create, amount, extras=None):
    # Calculates # of ore needed to make amount of create using chemicals
    if create == 'ORE':
        return [amount, extras]

    if extras == None:
        extras = {}

    r = chemicals[create]

    reactionNum = math.ceil(amount / r.outputs[create])

    total = 0
    for i in r.inputs:
        needed = r.inputs[i] * reactionNum
        if i in extras:
            needed -= extras[i]
            extras[i] = -needed if needed < 0 else 0

        if needed > 0:
            ore, extras = oreNeeded(chemicals, i, needed, extras)
            total += ore

    if create in extras:
        extras[create] += (r.outputs[create]) * reactionNum - amount
    else:
        extras[create] = (r.outputs[create]) * reactionNum - amount

    return [total, extras]

def main(verbose):
    with open('input.txt', encoding='UTF-8') as f:
        lines = [line.strip() for line in f.readlines()]

    reactions = []
    chemicals = {}
    for line in lines:
        reactions.append(reaction(line))

    for r in reactions:
        for o in r.outputs:
            chemicals[o] = r

    oneFuel = oreNeeded(chemicals, 'FUEL', 1)[0]

    ore = 1000000000000
    fuelMade = 0

    while True:
        fuelToMake = ore // oneFuel
        
        while True:
            oreUsed, extras = oreNeeded(chemicals, 'FUEL', fuelToMake)

            extrasSum = sum(extras.values())
            if oreUsed >= ore or extrasSum == 0:
                continuing = extrasSum == 0
                break

            fuelToMake += ((ore - oreUsed) // oneFuel) + 1

        if not continuing:
            fuelMade += fuelToMake - 1
            break

        amt = ore // oreUsed
        fuelMade += fuelToMake * amt
        ore -= oreUsed * amt

    if verbose:
        print(f"\nPart 1:\nAmount of ore needed to make 1 fuel: {oneFuel}\n\nPart 2:\nAmount of fuel made with one trillion ore: {fuelMade}")

    return [oneFuel, fuelMade]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds")
