import time
import numpy as np
import re

def printScreen(screen):
    string = ''
    for line in screen:
        string += '\n'
        for l in line:
            string += '@' if l == 1 else ' '

    return string

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    screen = np.zeros((6, 50), dtype=int)
    
    for line in lines:
        if line[1] == 'e':
            c, r = [int(x) for x in re.findall('\d+', line)]
            screen[0:r, 0:c] = 1
        elif 'x' in line:
            c, amt = [int(x) for x in re.findall('\d+', line)]
            screen = np.concatenate((screen[:, :c], np.transpose(np.atleast_2d(np.concatenate((screen[-amt:, c], screen[:-amt, c])))), screen[:, c+1:]), axis=1)
        elif 'y' in line:
            r, amt = [int(x) for x in re.findall('\d+', line)]
            screen = np.concatenate((screen[:r, :], np.atleast_2d(np.concatenate((screen[r, -amt:], screen[r, :-amt]))), screen[r+1:, :]), axis=0)

    print(f"\nPart 1:\nNumber of lit pixels: {sum(screen.flat)}")
    print(f"\nPart 2:\nMessage:\n{printScreen(screen)}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
