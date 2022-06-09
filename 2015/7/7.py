import time

class Component:
    def __init__(self, s):
        self.left, self.right = s.split(' -> ')
        self.left = self.left.split(' ')
        for i, l in enumerate(self.left):
            try:
                self.left[i] = int(l)
            except ValueError:
                pass

    def determineOutput(self, circuit, wires):
        if len(self.left) == 1:
            if self.left[0] in circuit:
                if self.left[0] not in wires:
                    wires[self.left[0]] = circuit[self.left[0]].determineOutput(circuit, wires)

                return wires[self.left[0]] % 65536
            else:
                return self.left[0] % 65536
        elif len(self.left) == 2:
            if self.left[1] in circuit:
                if self.left[1] not in wires:
                    wires[self.left[1]] = circuit[self.left[1]].determineOutput(circuit, wires)

                return (~wires[self.left[1]]) % 65536
            else:
                return (~self.left[1]) % 65536
        elif len(self.left) == 3:
            if self.left[0] in circuit:
                if self.left[0] not in wires:
                    wires[self.left[0]] = circuit[self.left[0]].determineOutput(circuit, wires)

                v1 = wires[self.left[0]]
            else:
                v1 = self.left[0]

            if self.left[2] in circuit:
                if self.left[2] not in wires:
                    wires[self.left[2]] = circuit[self.left[2]].determineOutput(circuit, wires)

                v2 = wires[self.left[2]]
            else:
                v2 = self.left[2]

            if self.left[1] == 'AND':
                return (v1 & v2) % 65536
            elif self.left[1] == 'OR':
                return (v1 | v2) % 65536
            elif self.left[1] == 'LSHIFT':
                return (v1 << v2) % 65536
            elif self.left[1] == 'RSHIFT':
                return (v1 >> v2) % 65536

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        circuit = {}
        for line in f.readlines():
            c = Component(line.strip('\n'))
            circuit[c.right] = c

    wires = {}
    wires['a'] = circuit['a'].determineOutput(circuit, wires)
    print(f"\nPart 1:\nValue in wire a after building the circuit: {wires['a']}")
    
    b = wires['a']
    wires = {}
    wires['b'] = b
    wires['a'] = circuit['a'].determineOutput(circuit, wires)
    print(f"\nPart 2:\nValue in wire a after overriding wire b: {wires['a']}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
