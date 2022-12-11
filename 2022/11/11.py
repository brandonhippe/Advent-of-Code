from time import perf_counter
import re


def add(a, n):
    return a + n


def mult(a, n):
    return a * n


def square(a, _):
    return a * a


def main(filename):
    with open(filename, encoding="UTF-8") as f:
        lines = [line.strip('\n') for line in f.readlines()]

    monkeyBusiness = {}
    monkeyOps = {}
    monkeyTests = {}

    items = []
    itemsP2 = []

    for line in lines:
        if "Monkey" in line:
            monkeyNum = [int(x) for x in re.findall("-?\d+", line)][0]
            monkeyBusiness[monkeyNum] = 0
        elif "Starting items" in line:
            items.append([])
            itemsP2.append([])
            for i in [int(x) for x in re.findall("-?\d+", line)]:
                items[-1].append(i)
                itemsP2[-1].append(i)
        elif "Operation" in line:
            if "old * old" in line:
                monkeyOps[monkeyNum] = [square, 0]
            elif "*" in line:
                monkeyOps[monkeyNum] = [mult, [int(x) for x in re.findall("-?\d+", line)][0]]
            else:
                monkeyOps[monkeyNum] = [add, [int(x) for x in re.findall("-?\d+", line)][0]]
        elif len(line) != 0:
            if monkeyNum not in monkeyTests:
                monkeyTests[monkeyNum] = []

            monkeyTests[monkeyNum].append([int(x) for x in re.findall("-?\d+", line)][0])


    for _ in range(20):
        for monkeyNum, monkeyItems in enumerate(items):
            items[monkeyNum] = []
            monkeyBusiness[monkeyNum] += len(monkeyItems)

            for item in monkeyItems:
                item = monkeyOps[monkeyNum][0](item, monkeyOps[monkeyNum][1])
                item //= 3

                if item % monkeyTests[monkeyNum][0] == 0:
                    items[monkeyTests[monkeyNum][1]].append(item)
                else:
                    items[monkeyTests[monkeyNum][2]].append(item)

    result = sorted(monkeyBusiness.values(), reverse=True)
        

    print(f"\nPart 1:\nMonkey Business after 20 rounds: {result[0] * result[1]}")

    items = itemsP2
    monkeyBusiness = {m: 0 for m in monkeyBusiness.keys()}

    monkeyMod = 1
    for i in range(len(monkeyBusiness)):
        monkeyMod *= monkeyTests[i][0]

    for _ in range(10000):
        for monkeyNum, monkeyItems in enumerate(items):
            items[monkeyNum] = []
            monkeyBusiness[monkeyNum] += len(monkeyItems)

            for item in monkeyItems:
                item = monkeyOps[monkeyNum][0](item, monkeyOps[monkeyNum][1])
                item %= monkeyMod

                if item % monkeyTests[monkeyNum][0] == 0:
                    items[monkeyTests[monkeyNum][1]].append(item)
                else:
                    items[monkeyTests[monkeyNum][2]].append(item)

    result = sorted(monkeyBusiness.values(), reverse=True)

    print(f"\nPart 2:\nMonkey Business after 10000 rounds: {result[0] * result[1]}")


if __name__ == "__main__":
    init_time = perf_counter()
    main("input.txt")
    print(f"\nRan in {perf_counter() - init_time} seconds.")