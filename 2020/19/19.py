import time
import re
from itertools import product

def messageLen(rule, rules, validLens):
    if isinstance(rules[rule], str):
        return [1, set()]

    total = 0
    recursRepeats = set()
    for i in range(len(rules[rule])):
        if rule in rules[rule][i]:
            recursRepeats.add(rule)
            continue

        for subRule in rules[rule][i]:
            if subRule not in validLens:
                validLens[subRule] = messageLen(subRule, rules, validLens)

            if i == 0:
                total += validLens[subRule][0]

            recursRepeats = recursRepeats.union(validLens[subRule][1])

    return [total, recursRepeats]

def valid(message, rule, rules, validLens, recursive):
    if isinstance(rules[rule], str):
        return message == rules[rule]

    if len(validLens[rule][1]) == 0 and len(message) != validLens[rule][0]:
        return False

    for subRules in rules[rule]:
        if not recursive and rule in subRules:
            continue

        for repeats in product(*([n for n in range(1, 2 + ((len(message) - validLens[rule][0]) // validLens[sR][0] if recursive and len(validLens[sR][1]) != 0 else 0))] for sR in subRules)):
            splits = [0]

            for mult, sR in zip(repeats, subRules):
                splits.append(splits[-1] + mult * validLens[sR][0])

            if splits[-1] == len(message) and all(valid(message[splits[i]:splits[i + 1]], subRules[i], rules, validLens, recursive) for i in range(len(subRules))):
                return True

    return False

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        data = [line.strip('\n') for line in f.readlines()]

    rules = {}
    messages = []
    for line in data:
        if len(messages) != 0 or len(line) == 0:
            messages.append(line)
            continue

        ruleNum, rText = line.split(':')
        if len(re.findall('\d+', rText)) != 0:
            rules[int(ruleNum)] = [[int(x) for x in re.findall('\d+', o)] for o in rText.split('|')]
        else:
            rules[int(ruleNum)] = rText.strip()

    messages.pop(0)

    rules[8].append([42, 8])
    rules[11].append([42, 11, 31])
    
    validLens = {}
    for r in rules.keys():
        if r not in validLens:
            validLens[r] = messageLen(r, rules, validLens)

    countP1, countP2 = 0, 0
    for m in messages:
        if valid(m, 0, rules, validLens, False):
            countP1 += 1
            countP2 += 1
        elif valid(m, 0, rules, validLens, True):
            countP2 += 1

    if verbose:
        print(f"\nPart 1:\nValid messages: {countP1}\n\nPart 2:\nValid messages: {countP2}")

    return [countP1, countP2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
