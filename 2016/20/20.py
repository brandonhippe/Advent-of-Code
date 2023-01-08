import time
import re

def intersections(r1, r2):
    return [(min(r1[0], r2[0]), max(r1[0], r2[0])), (max(r1[0], r2[0]), min(r1[1], r2[1])), (min(r1[1], r2[1]), max(r1[1], r2[1]))]

def main(verbose):
    filename = "input.txt"
    testing = '1' in filename
    with open(filename, encoding='UTF-8') as f:
        data = set(tuple(int(x) for x in re.findall('\d+', line)) for line in f.readlines())

    allowed = {(0, 10 if testing else 4294967295)}

    while len(data) > 0:
        low, high = list(data)[0]
        data.remove((low, high))
        changed = False
        for a in sorted(list(allowed)):
            allowed.remove(a)
            if a[0] > a[1] or low <= a[0] <= a[1] <= high:
                continue

            if a[0] <= low <= high <= a[1]:
                allowed.add((a[0], low - 1))
                allowed.add((high + 1, a[1]))
                changed = True
                break

            if a[0] <= low <= a[1]:
                allowed.add((a[0], low - 1))
                changed = True
                break

            if a[0] <= high <= a[1]:
                allowed.add((high + 1, a[1]))
                changed = True
                break

            allowed.add(a)

        if changed:
            data.add((low, high))

    allowed = sorted(list(allowed))

    part2 = sum([high - low + 1 for low, high in allowed])

    if verbose:
        print(f"\nPart 1:\nLowest allowed IP address: {allowed[0][0]}\n\nPart 2:\nTotal allowed IP addresses: {part2}")

    return [allowed[0][0], part2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
