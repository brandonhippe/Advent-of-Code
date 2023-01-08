import time
import re
import copy
import heapq

class Node:
    def __init__(self, name):
        self.name = name
        self.needs = []
        self.visited = False
        self.inProgress = False
        self.timeLeft = ord(self.name[1]) - ord('A') + 1

    def addNeed(self, other):
        self.needs.append(other)

    def available(self):
        for needed in self.needs:
            if not needed.visited:
                return False
        
        return True

    def __lt__(self, other):
        return ord(self.name[1]) < ord(other.name[1])

def order(nodes):
    free = []
    orderString = ''

    while len([n for n in nodes.values() if n.visited]) < len(nodes):
        for n in nodes.values():
            if n not in free and not n.visited and n.available():
                heapq.heappush(free, n)

        n = heapq.heappop(free)
        orderString += n.name[1:-1]
        n.visited = True

    return orderString

def orderTimed(nodes, numWorkers, baseTime):
    free = []
    freeWorkers = numWorkers
    for n in nodes.values():
        n.timeLeft += baseTime

    timeTaken = 0
    while len([n for n in nodes.values() if n.visited]) < len(nodes):
        for n in nodes.values():
            if n not in free and not n.visited and not n.inProgress and n.available():
                heapq.heappush(free, n)

        while len(free) > 0 and freeWorkers > 0:
            n = heapq.heappop(free)
            n.inProgress = True
            freeWorkers -= 1

        for n in nodes.values():
            if n.inProgress:
                n.timeLeft -= 1

                if n.timeLeft == 0:
                    n.visited = True
                    n.inProgress = False
                    freeWorkers += 1

        timeTaken += 1

    return timeTaken

def main(verbose):
    filename = "input.txt"
    with open(filename, encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    pattern = f"( {' | '.join(chr(c) for c in range(ord('A'), ord('Z') + 1)) } )"
    nodes = {}
    for line in lines:
        step, substep = re.findall(pattern, line)
        if step not in nodes:
            nodes[step] = Node(step)

        if substep not in nodes:
            nodes[substep] = Node(substep)

        nodes[substep].addNeed(nodes[step])

    part1 = order(copy.deepcopy(nodes))
    part2 = orderTimed(copy.deepcopy(nodes), 5 if len(re.findall('\d+', filename)) == 0 else 2, 60 if len(re.findall('\d+', filename)) == 0 else 0)
    
    if verbose:
        print(f"\nPart 1:\nCorrect Order: {part1}\n\nPart 2:\nTime Taken: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds")
