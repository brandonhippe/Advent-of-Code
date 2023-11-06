import time
import numpy as np


def main(verbose):
    filename = "input.txt"
    with open(filename, encoding='UTF-8') as f:
        rules = {l[0]: np.array([list(line) for line in l[1].split('/')]) for l in [line.strip('\n').split(' => ') for line in f.readlines()]}

    tempRules = rules.copy()

    for rule in tempRules.keys():
        r = np.array([list(line) for line in rule.split('/')])
        for i in range(7):
            r = np.flipud(r)
            if i % 2 == 1:
                r = np.rot90(r)

            rules['/'.join(''.join(line) for line in r)] = rules[rule]

    img = np.array([list(line) for line in ['.#.', '..#', '###']])

    for iterations in range(18 if '1' not in filename else 2):
        if iterations == 5:
            part1 = sum(sum(np.char.count(img, '#')))

        sz = 2 if len(img) % 2 == 0 else 3
        newImg = None
        for y in range(0, len(img), sz):
            lines = None
            for x in range(0, len(img[y]), sz):
                group = rules['/'.join(''.join(line) for line in img[y:y+sz, x:x+sz])]

                if lines is None:
                    lines = group
                else:
                    lines = np.concatenate((lines, group), axis=1)

            if newImg is None:
                newImg = lines
            else:
                newImg = np.concatenate((newImg, lines), axis=0)

        img = newImg

    part2 = sum(sum(np.char.count(img, '#')))

    if verbose:
        print(f"\nPart 1:\nNumber of lit pixels after 5 iterations: {part1}\n\nPart 2:\nNumber of lit pixels after 18 iterations: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
