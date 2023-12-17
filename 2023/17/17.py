from time import perf_counter
import heapq


def djikstra_p1(start, end, costs):
    openList = []
    openDict = {}
    closedDict = {}

    for d in [(0, 1), (1, 0)]:
        heapq.heappush(openList, (0, start, d, 0))
        openDict[(start, d, 0)] = 0

    while len(openList) != 0:
        pathLen, pos, d, d_moved = heapq.heappop(openList)
        del(openDict[(pos, d, d_moved)])

        if pos == end:
            return pathLen
        
        for offset in [d, (d[1], -d[0]), (-d[1], d[0])]:
            newPos = tuple(p + o for p, o in zip(pos, offset))
            if newPos not in costs:
                continue

            new_d_moved = d_moved + 1 if offset == d else 0

            if new_d_moved == 3:
                continue

            newPathLen = pathLen + costs[newPos]

            if (newPos, offset, new_d_moved) in openDict and openDict[(newPos, offset, new_d_moved)] <= newPathLen:
                continue

            if (newPos, offset, new_d_moved) in closedDict and closedDict[(newPos, offset, new_d_moved)] <= newPathLen:
                continue

            heapq.heappush(openList, (newPathLen, newPos, offset, new_d_moved))
            openDict[(newPos, offset, new_d_moved)] = newPathLen

        closedDict[(pos, d, d_moved)] = pathLen

    return -1


def djikstra_p2(start, end, costs):
    openList = []
    openDict = {}
    closedDict = {}

    for d in [(0, 1), (1, 0)]:
        heapq.heappush(openList, (0, start, d, 0))
        openDict[(start, d, 0)] = 0

    while len(openList) != 0:
        pathLen, pos, d, d_moved = heapq.heappop(openList)
        del(openDict[(pos, d, d_moved)])

        if pos == end and d_moved >= 3:
            return pathLen
        
        if d_moved < 3:
            new_dirs = [d]
        else:
            new_dirs = [d, (d[1], -d[0]), (-d[1], d[0])]
        
        for offset in new_dirs: 
            newPos = tuple(p + o for p, o in zip(pos, offset))
            if newPos not in costs:
                continue

            new_d_moved = d_moved + 1 if offset == d else 0

            if new_d_moved == 10:
                continue

            newPathLen = pathLen + costs[newPos]

            if (newPos, offset, new_d_moved) in openDict and openDict[(newPos, offset, new_d_moved)] <= newPathLen:
                continue

            if (newPos, offset, new_d_moved) in closedDict and closedDict[(newPos, offset, new_d_moved)] <= newPathLen:
                continue

            heapq.heappush(openList, (newPathLen, newPos, offset, new_d_moved))
            openDict[(newPos, offset, new_d_moved)] = newPathLen

        closedDict[(pos, d, d_moved)] = pathLen

    return -1


def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    losses = {}
    for y, line in enumerate(lines):
        for x, l in enumerate(line):
            losses[(x, y)] = int(l)

    part1 = djikstra_p1((0, 0), (len(lines[0]) - 1, len(lines) - 1), losses)
    part2 = djikstra_p2((0, 0), (len(lines[0]) - 1, len(lines) - 1), losses)

    if verbose:
        print(f"\nPart 1:\n{part1}\n\nPart 2:\n{part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = perf_counter()
    main(True)
    print(f"\nRan in {perf_counter() - init_time} seconds.")
