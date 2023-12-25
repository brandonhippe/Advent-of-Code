from time import perf_counter
from collections import defaultdict
from functools import cache
from itertools import product
import re


rules = defaultdict(lambda: [])


def andConds(mainCond, otherCond):
    newConds = {k: [] for k in 'xmas'}
    for spec, conds in mainCond.items():
        if spec not in otherCond or len(otherCond[spec]) == 0:
            newConds[spec] = conds
            continue

        for (mainMin, mainMax), (otherMin, otherMax) in product(conds, otherCond[spec]):
            newConds[spec].append([max(mainMin, otherMin), min(mainMax, otherMax)])

    return newConds


def orConds(mainCond, otherCond):
    newConds = {k: [] for k in 'xmas'}
    for spec, conds in mainCond.items():
        newConds[spec] += conds

    for spec, conds in otherCond.items():
        newConds[spec] += conds

    return newConds


@cache
def ruleCombs(rule):
    if rule == 'A':
        return {k: [[1, 4000]] for k in 'xmas'}
    
    if rule == 'R':
        return {k: [] for k in 'xmas'}
    
    ruleConds = {k: [] for k in 'xmas'}
    for cond, dest in rules[rule][::-1]:
        try:
            op = re.findall('[<>]+', cond)[0]
            spec, val = cond.split(op)
            val = int(val)

            if op == '<':
                cond = {spec: [[1, val - 1]]}
                notCond = {spec: [[val, 4000]]}
            else:
                cond = {spec: [[val + 1, 4000]]}
                notCond = {spec: [[1, val]]}

            ruleConds = andConds(ruleConds, notCond)

            destCond = ruleCombs(dest)
            destCond = andConds(destCond, cond)
        except IndexError:
            destCond = ruleCombs(dest)

        ruleConds = orConds(ruleConds, destCond)

    return ruleConds


def evalWorkflow(workflow, x, m, a, s):
    while workflow not in 'AR':
        for cond, dest in rules[workflow]:
            if eval(cond):
                workflow = dest
                break

    return workflow == 'A'


def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    ix = 0
    while len(lines[ix]) != 0:
        name, ruleInfo = lines[ix][:-1].split('{')
        ruleInfo = ruleInfo.split(',')

        for r in ruleInfo:
            try:
                cond, next = r.split(':')
            except ValueError:
                cond, next = 'True', r

            rules[name].append([cond, next])

        ix += 1

    part1 = 0
    for line in lines[ix + 1:]:
        x, m, a, s = [int(n) for n in re.findall('\d+', line)]

        if evalWorkflow('in', x, m, a, s):
            part1 += x+m+a+s

    part2 = 0
    accepted = ruleCombs('in')

    for i in range(len(accepted['x'])):
        rs = [accepted[k][i] for k in 'xmas']
        product = 1
        for small, big in rs:
            product *= (big - small + 1)

        part2 += product

    if verbose:
        print(f"\nPart 1:\nSum of Accepted Ratings: {part1}\n\nPart 2:\nTotal combinations accepted: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")
