import time

def main(verbose):
    with open('input.txt', encoding='UTF-8') as f:
        lines = [line.strip() for line in f.readlines()]

    template = lines[0]
    templatePairs = [template[i:i+2] for i in range(0, len(template) - 1)]
    pairs = {}
    for pair in templatePairs:
        if pair in pairs:
            pairs[pair] += 1
        else:
            pairs[pair] = 1
    
    lines = lines[2:]

    occurrances = {}
    for t in template:
        if t in occurrances:
            occurrances[t] += 1
        else:
            occurrances[t] = 1

    insertions = {}
    for line in lines:
        line = line.split(" -> ")
        insertions[line[0]] = line[1]

    for _ in range(10):
        nextPairs = pairs.copy()
        for pair in pairs:
            newLetter = insertions[pair]
            if newLetter in occurrances:
                occurrances[newLetter] += pairs[pair]
            else:
                occurrances[newLetter] = pairs[pair]

            newPairs = [pair[0] + newLetter, newLetter + pair[1]]
            nextPairs[pair] -= pairs[pair]
            for nP in newPairs:
                if nP in nextPairs:
                    nextPairs[nP] += pairs[pair]
                else:
                    nextPairs[nP] = pairs[pair]

        pairs = nextPairs.copy()
    
    counts = []
    for o in occurrances:
        counts.append(occurrances[o])
    counts.sort()

    part1 = counts[-1] - counts[0]

    for _ in range(30):
        nextPairs = pairs.copy()
        for pair in pairs:
            newLetter = insertions[pair]
            if newLetter in occurrances:
                occurrances[newLetter] += pairs[pair]
            else:
                occurrances[newLetter] = pairs[pair]

            newPairs = [pair[0] + newLetter, newLetter + pair[1]]
            nextPairs[pair] -= pairs[pair]
            for nP in newPairs:
                if nP in nextPairs:
                    nextPairs[nP] += pairs[pair]
                else:
                    nextPairs[nP] = pairs[pair]

        pairs = nextPairs.copy()
    
    counts = []
    for o in occurrances:
        counts.append(occurrances[o])
    counts.sort()

    if verbose:
        print(f"\nPart 1:\nMost common - least common = {part1}\n\nPart 2:\nMost common - least common = {counts[-1] - counts[0]}")

    return [part1, counts[-1] - counts[0]]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds")
