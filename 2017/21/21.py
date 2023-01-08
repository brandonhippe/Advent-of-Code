import time
import numpy as np
import copy

def main(verbose):
    filename = "input.txt"
    with open(filename, encoding='UTF-8') as f:
        rules = {l[0]: l[1] for l in [line.strip('\n').split(' => ') for line in f.readlines()]}

    tempRules = copy.deepcopy(rules)

    for rule in tempRules.keys():
        r = np.array([[c for c in line] for line in rule.split('/')])
        for i in range(7):
            r = np.flipud(r)
            if i % 2 == 1:
                r = np.rot90(r)

            rules['/'.join(''.join(line) for line in r)] = rules[rule]

    img = np.array([[c for c in line] for line in ['.#.', '..#', '###']])

    for iterations in range(18 if '1' not in filename else 2):
        sz = 2 if len(img) % 2 == 0 else 3
        for y in range(0, len(img), sz):
            for x in range(0, len(img[y]), sz):
                group = np.array([[c for c in l] for l in rules['/'.join(''.join(line) for line in img[y:y+sz, x:x+sz])].split('/')])
                if x == 0:
                    lines = group
                else:
                    lines = np.concatenate((lines, group), axis=1)

            if y == 0:
                newImg = lines
            else:
                newImg = np.concatenate((newImg, lines), axis=0)

        img = newImg

        if iterations == 4:
            part1 = sum(sum(np.char.count(img, '#')))

    part2 = sum(sum(np.char.count(img, '#')))

    if verbose:
        print(f"\nPart 1:\nNumber of lit pixels after 5 iterations: {part1}\n\nPart 1:\nNumber of lit pixels after 18 iterations: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
