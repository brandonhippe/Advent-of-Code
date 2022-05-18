import time
import re
from collections import defaultdict

class Rule:
    def __init__(self):
        self.operations = {0: [], 1: []}

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    state = lines[0].split('state ')[1][:-1]
    iterations = int(re.findall('\d+', lines[1])[0])

    stateRules = {}
    for i, line in enumerate(lines[3:]):        
        if i % 10 == 0:
            currState = line.split('state ')[1][:-1]
            stateRules[currState] = Rule()
        elif i % 10 in [1, 5]:
            currValue = int(re.findall('\d+', line)[0])
        elif i % 10 in [2, 6]:
            stateRules[currState].operations[currValue].append(int(re.findall('\d+', line)[0]))
        elif i % 10 in [3, 7]:
            stateRules[currState].operations[currValue].append(1 if 'right' in line else -1)
        elif i % 10 in [4, 8]:
            stateRules[currState].operations[currValue].append(line.split('state ')[1][:-1])

    tape = defaultdict(lambda: 0)
    cursor = 0
    for _ in range(iterations):
        newVal, cursorInc, newState = stateRules[state].operations[tape[cursor]]
        tape[cursor] = newVal
        cursor += cursorInc
        state = newState

    print(f"\nPart 1:\nChecksum: {sum(tape.values())}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
