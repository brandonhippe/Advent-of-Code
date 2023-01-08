import time
import re
from collections import defaultdict

class Program:
    def __init__(self, programText):
        self.weight = int(re.findall('\d+', programText)[0])
        self.name = programText.split(' ')[0]
        self.subPrograms = []
        if '->' in programText:
            self.subPrograms = programText.split('-> ')[1].split(', ')

    def genWeight(self):
        return sum([self.weight] + [s.genWeight() for s in self.subPrograms])

    def balance(self):
        subWeights = defaultdict(lambda: [])
        for s in self.subPrograms:
            subWeights[s.genWeight()].append(s)

        for w, s in zip(subWeights.keys(), subWeights.values()):
            if len(s) == 1:
                subBalanced = s[0].balance()
                if subBalanced == 0:
                    ow = list(o for o in subWeights.keys() if o != w)[0]
                    return s[0].weight + ow - w
                else:
                    return subBalanced

        return 0

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        programs = [Program(line.strip('\n')) for line in f.readlines()]

    pNames = {p.name for p in programs}
    for p in programs:
        for s in p.subPrograms:
            if s in pNames:
                pNames.remove(s)

    head = list(pNames)[0]

    part1 = head

    programs = {p.name: p for p in programs}
    for p in programs.values():
        for i, s in enumerate(p.subPrograms):
            p.subPrograms[i] = programs[s]

    part2 = programs[head].balance()

    if verbose:
        print(f"\nPart 1:\nName of bottom program: {part1}\n\nPart 2:\nWeight of unbalanced program needed to balance: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
