from time import perf_counter
from collections import defaultdict
import re


OFFSETS = {'R': (1, 0), 'D': (0, 1), 'L': (-1, 0), 'U': (0, -1)}


def enclosedArea(adjacencies, xs, ys):
    total = 0
    xs = sorted(xs)
    ys = sorted(ys)

    for i, y in enumerate(ys):
        inside_line = False
        first_line = True
        collected_line = None

        inside_area = False

        for x in xs:
            ### Handle areas above this line, up to but not including previous line
            if (x, y) in adjacencies:
                for n in adjacencies[(x, y)]:
                    if n[1] != y and n[1] < y:
                        if inside_area:
                            inside_area = False
                            total += (y - ys[i - 1] - 1) * (x - px_area + 1)
                        else:
                            inside_area = True
                            px_area = x

                        break
            else:
                toggled = False
                for y1 in ys[:i]:
                    if (x, y1) not in adjacencies:
                        continue

                    for n in adjacencies[(x, y1)]:
                        if y < n[1]:
                            if inside_area:
                                inside_area = False
                                total += (y - ys[i - 1] - 1) * (x - px_area + 1)
                            else:
                                inside_area = True
                                px_area = x

                            toggled = True
                            break

                    if toggled:
                        break
                        
            ### Handle areas on this line
            if (x, y) in adjacencies:
                if collected_line is None:
                    if not inside_line:
                        inside_line = True
                        px_line = x

                    for n in adjacencies[(x, y)]:
                        if n[1] != y:
                            collected_line = abs(n[1] - y) // (n[1] - y)
                            break
                else:
                    for n in adjacencies[(x, y)]:
                        if n[1] != y:
                            if ((abs(n[1] - y) // (n[1] - y)) != collected_line) ^ first_line:
                                inside_line = False
                                first_line = True
                                total += x - px_line + 1
                            else:       
                                first_line = False

                            collected_line = None
                            break
            else:
                toggled = False
                for y1 in ys[:i]:
                    if (x, y1) not in adjacencies:
                        continue

                    for n in adjacencies[(x, y1)]:
                        if y < n[1]:
                            if inside_line:
                                inside_line = False
                                first_line = True
                                total += x - px_line + 1
                            else:
                                inside_line = True
                                first_line = False
                                px_line = x

                            toggled = True
                            break

                    if toggled:
                        break

    return total


def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]
    
    pos_p1 = (0, 0)
    adjacencies_p1 = defaultdict(lambda: set())
    xs_p1 = set()
    ys_p1 = set()

    pos_p2 = (0, 0)
    adjacencies_p2 = defaultdict(lambda: set())
    xs_p2 = set()
    ys_p2 = set()

    for line in lines:
        prev_p1 = pos_p1
        direction, dist, color = line.split(' ')
        pos_p1 = tuple(p + (o * int(dist)) for p, o in zip(pos_p1, OFFSETS[direction]))
        xs_p1.add(pos_p1[0])
        ys_p1.add(pos_p1[1])
        adjacencies_p1[pos_p1].add(prev_p1)
        adjacencies_p1[prev_p1].add(pos_p1)

        prev_p2 = pos_p2
        dist = re.findall('\w+', color)[0]
        direction = list(OFFSETS.keys())[int(dist[-1])]
        dist = int(dist[:-1], 16)
        pos_p2 = tuple(p + (o * dist) for p, o in zip(pos_p2, OFFSETS[direction]))
        xs_p2.add(pos_p2[0])
        ys_p2.add(pos_p2[1])
        adjacencies_p2[pos_p2].add(prev_p2)
        adjacencies_p2[prev_p2].add(pos_p2)

    part1 = enclosedArea(adjacencies_p1, xs_p1, ys_p1)
    part2 = enclosedArea(adjacencies_p2, xs_p2, ys_p2)

    if verbose:
        print(f"\nPart 1:\nEnclosed Area: {part1}\n\nPart 2:\nEnclosed Area: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")
