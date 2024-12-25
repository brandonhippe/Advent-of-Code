from collections import defaultdict

def part1(data):
    """ 2015 Day 9 Part 1

    >>> part1(['London to Dublin = 464', 'London to Belfast = 518', 'Dublin to Belfast = 141'])
    605

    """

    adj = defaultdict(lambda: {})

    for line in data:
        n1, _, n2, _, dist = line.split(' ')
        adj[n1][n2] = int(dist)
        adj[n2][n1] = int(dist)

    return shortestPath(adj)


def part2(data):
    """ 2015 Day 9 Part 2

    >>> part2(['London to Dublin = 464', 'London to Belfast = 518', 'Dublin to Belfast = 141'])
    982

    """

    adj = defaultdict(lambda: {})

    for line in data:
        n1, _, n2, _, dist = line.split(' ')
        adj[n1][n2] = int(dist)
        adj[n2][n1] = int(dist)

    return longestPath(adj)


def shortestPath(adj, collected = [], memo = {}):
    if len(collected) == len(adj):
        return 0

    shortest = float('inf')
    for n in adj.keys():
        if n in collected:
            continue

        if tuple(collected + [n]) not in memo:
            memo[tuple(collected + [n])] = shortestPath(adj, collected + [n], memo)

        total = memo[tuple(collected + [n])] + (adj[collected[-1]][n] if len(collected) > 0 else 0)
        if total < shortest:
            shortest = total

    return shortest


def longestPath(adj, collected = [], memo = {}):
    if len(collected) == len(adj):
        return 0

    longest = float('-inf')
    for n in adj.keys():
        if n in collected:
            continue

        if tuple(collected + [n]) not in memo:
            memo[tuple(collected + [n])] = longestPath(adj, collected + [n], memo)

        total = memo[tuple(collected + [n])] + (adj[collected[-1]][n] if len(collected) > 0 else 0)
        if total > longest:
            longest = total

    return longest


def main(verbose = False):
    from pathlib import Path
    import sys, re
    sys.path.append(str(Path(__file__).parent.parent.parent))
    from Modules.timer import Timer
    year, day = re.findall('\d+', str(__file__))[-2:]
    
    with open(Path(__file__).parent.parent.parent / f"Inputs/{year}_{day}.txt", encoding='UTF-8') as f:
        data = [line.strip('\n') for line in f.readlines()]
    
    with Timer() as p1_time:
        p1 = part1(data)

    if verbose:
        print(f"\nPart 1:\nShortest path to all locations: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nLongest path to all locations: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)