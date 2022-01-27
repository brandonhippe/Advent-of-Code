import math
import time

class moon:
    def __init__(self, pos, num):
        self.pos = pos[:]
        self.vel = [0] * len(self.pos)
        self.number = num

    def gravity(self, others):
        for other in others:
            if other == self:
                continue

            delta = []
            for (selfC, otherC) in zip(self.pos, other.pos):
                delta.append(selfC - otherC)

            for (i, d) in enumerate(delta):
                self.vel[i] += 1 if d < 0 else (-1 if d > 0 else 0)

    def timeStep(self):
        for (i, v) in enumerate(self.vel):
            self.pos[i] += v

    def potEng(self):
        return sum(abs(x) for x in self.pos)

    def kinEng(self):
        return sum(abs(x) for x in self.vel)

    def totEng(self):
        return self.potEng() * self.kinEng()

def axisState(moons, axis):
    string = str(moons[0].pos[axis]) + ',' + str(moons[0].vel[axis])
    for m in moons[1:]:
        string += ',' + str(m.pos[axis]) + ',' + str(m.vel[axis])

    return string

def lcm(arr):
    while len(arr) > 2:
        arr.append(lcm([arr.pop(-1) for _ in range(2)]))

    return abs(arr[0] * arr[1]) // math.gcd(arr[0], arr[1])

def main():
    with open('input.txt', encoding='UTF-8') as f:
        lines = [line.strip("<>\n") for line in f.readlines()]

    moons = []
    for line in lines:
        moons.append(moon([int(x.split("=")[-1]) for x in line.split(",")], len(moons)))

    steps = 1000

    for _ in range(steps):
        totalEnergy = 0
        for m in moons:
            m.gravity(moons)

        for m in moons:
            m.timeStep()
            totalEnergy += m.totEng()

    print(f"\nPart 1:\nTotal Energy: {totalEnergy}")

    moons = []
    for line in lines:
        moons.append(moon([int(x.split("=")[-1]) for x in line.split(",")], len(moons)))

    step = 0
    cycles = [float('inf')] * 3
    states = []
    for a in range(3):
        temp = {}
        temp[axisState(moons, a)] = step
        states.append(temp)

    while sum(cycles) == float('inf'):
        for m in moons:
            m.gravity(moons)

        for m in moons:
            m.timeStep()

        step += 1

        for a in range(3):
            if cycles[a] == float('inf'):
                state = axisState(moons, a)
                if state in states[a]:
                    cycles[a] = step - states[a][state]
                else:
                    states[a][state] = step

    print(f"\nPart 2:\nFirst repeated postions will occur at step {lcm(cycles)}, found at step {step}")

init_time = time.perf_counter()
main()
print(f"\nRan in {time.perf_counter() - init_time} seconds")
