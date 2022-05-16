import time
import re

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        data = f.readline().strip('\n').split(',')

    programs = [chr(n + ord('a')) for n in range(16)]
    
    i = 0
    states = {}
    while i < 1_000_000_000:
        for d in data:
            if d[0] == 's':
                n = int(re.findall('\d+', d)[0])
                programs = programs[-n:] + programs[:-n]
            elif d[0] == 'x':
                nums = [int(x) for x in re.findall('\d+', d)]
                programs[nums[0]], programs[nums[1]] = programs[nums[1]], programs[nums[0]]
            elif d[0] == 'p':
                nums = (programs.index(d[1]), programs.index(d[-1]))
                programs[nums[0]], programs[nums[1]] = programs[nums[1]], programs[nums[0]]

        string = ''.join(programs)

        if i == 0:
            print(f"\nPart 1:\nOrder after dance: {string}")

        if string in states:
            i += (1_000_000_000 - i) // (i - states[string]) * (i - states[string])
            
        states[string] = i

        i += 1

    print(f"\nPart 2:\nOrder after a billion dances: {string}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
