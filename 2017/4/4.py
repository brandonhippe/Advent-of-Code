import time

def validP2(lines):
    total = 0

    for line in lines:
        words = set()
        for w in line:
            d = tuple(sorted(((c, w.count(c)) for c in w), key=lambda e: e[0]))
            if d not in words:
                words.add(d)
        
        if len(words) == len(line):
            total += 1

    return total

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n').split(' ') for line in f.readlines()]

    part1 = sum([1 if len(set(l for l in line)) == len(line) else 0 for line in lines])
    part2 = validP2(lines)

    if verbose:
        print(f"\nPart 1:\nValid passphrases: {part1}\n\nPart 2:\nValid passphrases: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
