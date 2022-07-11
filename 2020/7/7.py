import time
import re

class Bag:
    def __init__(self, bagText):
        bagCounts = [int(x) for x in re.findall('\d+', bagText)]
        data = re.split(' bag?s |, ', bagText)

        self.name = data[0]
        self.bags = {}
        if len(bagCounts) > 0:
            for i, text in enumerate(data[1:]):
                start = re.search('\d+', text).span()[1] + 1
                end = re.search('bag', text).span()[0] - 1
                self.bags[text[start:end]] = bagCounts[i]

    def canContain(self, allBags, goal):
        if self.name == goal:
            return True

        for b in self.bags.keys():
            if allBags[b].canContain(allBags, goal):
                return True

        return False

    def numContained(self, allBags, memo):
        total = 0
        for b, amt in zip(self.bags.keys(), self.bags.values()):
            if b not in memo:
                memo[b] = allBags[b].numContained(allBags, memo)

            total += amt * (1 + memo[b])

        return total

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        bags = {Bag(line.strip('\n')).name: Bag(line.strip('\n')) for line in f.readlines()}

    print(f"\nPart 1:\nNumber of bags that can contain a shiny gold bag: {len([b for b in bags.values() if b.canContain(bags, 'shiny gold')]) - 1}")
    print(f"\nPart 2:\nNumber of bags contained within a shiny gold bag: {bags['shiny gold'].numContained(bags, {})}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
