from time import perf_counter
from collections import deque


def mix(correctOrder, indexes):
    for i in range(len(correctOrder)):
        loc = indexes.index(i)
        correctOrder.rotate(-loc)
        indexes.rotate(-loc)

        n = correctOrder.popleft()
        ix = indexes.popleft()

        correctOrder.rotate(-n)
        indexes.rotate(-n)

        correctOrder.appendleft(n)
        indexes.appendleft(ix)

    return [correctOrder, indexes]


def getCoordinateSum(correctOrder):
    correctOrder.rotate(-correctOrder.index(0))
    s = [correctOrder[i] for i in [1000, 2000, 3000]]
    return sum(s)


def main(filename):
    with open(filename, encoding="UTF-8") as f:
        lines = [int(line.strip('\n')) for line in f.readlines()]

    indexes = deque(range(len(lines)))
    correctOrder = deque(lines[:])

    correctOrder = mix(correctOrder, indexes)[0]
    
    print(f"\nPart 1:\n{getCoordinateSum(correctOrder)}")

    indexes = deque(range(len(lines)))
    correctOrder = deque([n * 811589153 for n in lines])

    for _ in range(10):
        correctOrder, indexes = mix(correctOrder, indexes)

    print(f"\nPart 2:\n{getCoordinateSum(correctOrder)}")


if __name__ == "__main__":
    init_time = perf_counter()
    main("input.txt")
    print(f"\nRan in {perf_counter() - init_time} seconds.")