import time
import re

class Node:
    def __init__(self):
        self.subNodes = []
        self.metadata = []

    def parse(self, input):
        numChildren, numData = input[:2]
        input = input[2:]

        for _ in range(numChildren):
            self.subNodes.append(Node())
            input = self.subNodes[-1].parse(input)

        self.metadata = input[:numData]
        return input[numData:]

    def metadataSum(self):
        return sum([c.metadataSum() for c in self.subNodes]) + sum(self.metadata)

    def evaluate(self):
        if len(self.subNodes) == 0:
            return sum(self.metadata)

        total = 0
        for n in self.metadata:
            i = n - 1
            if i < len(self.subNodes):
                total += self.subNodes[i].evaluate()

        return total

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        data = [int(x) for x in re.findall('\d+', f.readline().strip('\n'))]

    tree = Node()
    tree.parse(data[:])

    print(f"\nPart 1:\nSum of metadata entries: {tree.metadataSum()}")
    print(f"\nPart 2:\nValue of root node: {tree.evaluate()}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
