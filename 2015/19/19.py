import time
import re

def reverseMoleculeCreation(molecule, backtrackRules):
    if molecule == 'e':
        return 0
    
    for k, v in backtrackRules:
        if k in molecule:
            result = reverseMoleculeCreation(molecule.replace(k, v, 1), backtrackRules)
            if result is not None:
                return result + 1

    return None

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    string = lines[-1]
    rules = {line.split(' => ')[0]: [] for line in lines[:-2]}
    for line in lines[:-2]:
        line = line.split(' => ')
        rules[line[0]].append(line[1])

    oneStep = set()
    for r in rules.keys():
        end = 0
        o = re.search(r, string)
        while o:
            start, newend = o.span()
            start += end
            end += newend
            for rep in rules[r]:
                oneStep.add(string[:start] + rep + string[end:])

            o = re.search(r, string[end:])

    part1 = len(oneStep)

    backtrackRules = {}
    for k, v in zip(rules.keys(), rules.values()):
        for s in v:
            backtrackRules[s] = k

    part2 = reverseMoleculeCreation(string, sorted(list(zip(backtrackRules.keys(), backtrackRules.values())), key=lambda e: len(e[0]), reverse=True))

    if verbose:
        print(f"\nPart 1:\nNumber of molecules that can be made with a single replacement: {part1}\n\nPart 2:\nFewest steps to create molecule: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
