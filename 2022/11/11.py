from time import perf_counter
import re


class Monkey:
    def __init__(self, number) -> None:
        self.number = number
        self.items = []
        self.op = []
        self.test = []
        self.inspections = 0


    def __hash__(self) -> int:
        return self.number


    def __lt__(self, other):
        return self.inspections < other.inspections


    def throw(self, otherMonkeys, div3 = True):
        self.items.reverse()

        while len(self.items) != 0:
            self.inspections += 1
            self.items[-1] = self.op[0](self.items[-1], self.op[1])

            if div3:
                self.items[-1] //= 3

            if self.items[-1] % self.test[0] == 0:
                otherMonkeys[self.test[1]].items.append(self.items.pop())
            else:
                otherMonkeys[self.test[2]].items.append(self.items.pop())


def add(n, a):
    return n + a


def mult(n, a):
    return n * a


def square(n, _):
    return n * n


def main(filename):
    with open(filename, encoding="UTF-8") as f:
        lines = [line.strip('\n') for line in f.readlines()]

    monkeys = {}

    for line in lines:
        if len(line) == 0:
            continue
        elif line[0] == 'M':
            monkeys[len(monkeys)] = Monkey(len(monkeys))
            monkeyLine = 0
            continue
        
        if monkeyLine == 0:
            monkeys[len(monkeys) - 1].items = [int(x) for x in re.findall("-?\d+", line)]
        elif monkeyLine == 1:
            if "old * old" in line:
                monkeys[len(monkeys) - 1].op = [square, 0]
            elif "old *" in line:
                monkeys[len(monkeys) - 1].op = [mult, [int(x) for x in re.findall("-?\d+", line)][0]]
            else:
                monkeys[len(monkeys) - 1].op = [add, [int(x) for x in re.findall("-?\d+", line)][0]]
        elif monkeyLine >= 2:
            monkeys[len(monkeys) -1].test.append([int(x) for x in re.findall("-?\d+", line)][0])

        monkeyLine += 1


    for _ in range(20):
        for i in range(len(monkeys)):
            monkeys[i].throw(monkeys)

    monkeyBusiness = sorted(list(monkeys.values()), reverse=True)

    print(f"\nPart 1:\n{monkeyBusiness[0].inspections * monkeyBusiness[1].inspections}")

    for _ in range(10000):
        for i in range(len(monkeys)):
            monkeys[i].throw(monkeys, False)

    monkeyBusiness = sorted(list(monkeys.values()), reverse=True)

    print(f"\nPart 2:\n{monkeyBusiness[0].inspections * monkeyBusiness[1].inspections}")


if __name__ == "__main__":
    init_time = perf_counter()
    main("input.txt")
    print(f"\nRan in {perf_counter() - init_time} seconds.")