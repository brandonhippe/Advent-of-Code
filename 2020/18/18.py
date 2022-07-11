import time
from copy import deepcopy

class Expression:
    def __init__(self, text, sub=False):
        if sub:
            text = text[1:-1]

        self.ops = []
        self.vals = []
        bits = text.split(' ')
        i = 0
        while i < len(bits):
            if bits[i][0] == '(':
                opened = 0
                for c in bits[i]:
                    if c == '(':
                        opened += 1

                j = i + 1
                while opened != 0:
                    for c in bits[j]:
                        if c == '(':
                            opened += 1
                        elif c == ')':
                            opened -= 1

                    j += 1

                self.vals.append(Expression(' '.join(bits[i:j]), True))
                i = j
            else:
                try:
                    self.vals.append(int(bits[i]))
                except ValueError:
                    self.ops.append(bits[i])

                i += 1

    def evalP1(self):
        self.ops.reverse()
        self.vals.reverse()
        while len(self.vals) != 1:
            left = self.vals.pop(-1)
            right = self.vals.pop(-1)
            if isinstance(left, Expression):
                left = left.evalP1()

            if isinstance(right, Expression):
                right = right.evalP1()

            op = self.ops.pop(-1)

            if op == '+':
                self.vals.append(left + right)
            else:
                self.vals.append(left * right)

        return self.vals[0]

    def evalP2(self):
        for i, v in enumerate(self.vals):
            if isinstance(v, Expression):
                self.vals[i] = v.evalP2()

        for i, op in enumerate(self.ops):
            if op == '+':
                self.vals = self.vals[:i] + [1, self.vals[i] + self.vals[i + 1]] + self.vals[i + 2:]

        product = 1
        for v in self.vals:
            product *= v

        return product

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        data = [Expression(line.strip('\n')) for line in f.readlines()]

    print(f"\nPart 1:\nSum of evaluated expressions: {sum([e.evalP1() for e in deepcopy(data)])}")
    print(f"\nPart 2:\nSum of evaluated expressions: {sum([e.evalP2() for e in data])}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
