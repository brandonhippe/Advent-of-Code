import time
from collections import defaultdict

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    countP1, countP2 = 0, 0
    group = defaultdict(lambda: 0)
    inGroup = 0
    for line in lines:
        if len(line) == 0:
            countP1 += len(group)
            countP2 += len([g for g in list(group.keys()) if group[g] == inGroup])

            group = defaultdict(lambda: 0)
            inGroup = 0
            continue
        
        inGroup += 1
        for c in line:
            group[c] += 1

    print(f"\nPart 1:\nNumber of questions answered yes: {countP1}")
    print(f"\nPart 2:\nNumber of questions answered yes by everyone in a group: {countP2}")
    
if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
