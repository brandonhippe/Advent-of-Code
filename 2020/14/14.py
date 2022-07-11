import time
import re

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        data = [line.strip('\n') for line in f.readlines()]

    mem_1 = {}
    mem_2 = {}
    for line in data:
        if line[1] == 'a':
            mask = re.split(' ', line)[-1]
        else:
            addr, val = [int(x) for x in re.findall('\d+', line)]
            ones = int(''.join(['1' if c == '1' else '0' for c in mask]), 2)
            zeros = int(''.join(['0' if c == '0' else '1' for c in mask]), 2)
            mem_1[addr] = (val & zeros) | ones


            baseAddr = list('0' * (36 - len(bin(addr | ones)[2:])) + bin(addr | ones)[2:])
            for n in range(2 ** len([c for c in mask if c == 'X'])):
                b = '0' * (len([c for c in mask if c == 'X']) - len(bin(n)[2:])) + bin(n)[2:]
                addr = baseAddr[:]
                j = 0
                for i, c in enumerate(mask):
                    if c == 'X':
                        addr[i] = b[j]
                        j += 1

                mem_2[int(''.join(addr), 2)] = val

    print(f"\nPart 1:\nSum of all values in memory: {sum(list(mem_1.values()))}")
    print(f"\nPart 2:\nSum of all values in memory: {sum(list(mem_2.values()))}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
