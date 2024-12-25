import numpy as np
from collections import defaultdict


def part1(data):
    """ 2023 Day 25 Part 1

    >>> part1(['jqt: rhn xhk nvd', 'rsh: frs pzl lsr', 'xhk: hfx', 'cmg: qnr nvd lhk bvb', 'rhn: xhk bvb hfx', 'bvb: xhk hfx', 'pzl: lsr hfx nvd', 'qnr: nvd', 'ntq: jqt hfx bvb xhk', 'nvd: lhk', 'lsr: lhk', 'rzs: qnr cmg lsr rsh', 'frs: qnr lhk lsr'])
    54
    """

    connections = defaultdict(lambda: set())
    connectionSet = set()
    for line in data:
        name, conns = line.split(": ")
        for c in conns.split(' '):
            connections[name].add(c)
            connections[c].add(name)
            connectionSet.add(tuple(sorted([name, c])))

    indexes = {k: i for i, k in enumerate(connections.keys())}

    arrDim = len(connections)
    degree = np.zeros((arrDim, arrDim))
    adj = np.zeros((arrDim, arrDim))

    for k, i in indexes.items():
        degree[i][i] = len(connections[k])
        
        for n in connections[k]:
            j = indexes[n]
            adj[i][j] = 1

    laplacian = degree - adj
    v = np.linalg.svd(laplacian)[2]
    fiedler = v[-2]
    gSize = len([g for g in fiedler if g > 0])

    return gSize * (arrDim - gSize)


def part2(data):
    """ 2023 Day 25 Part 2
    """

    return 1


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
        print(f"\nPart 1:\nProduct of disconnected group sizes: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nChristmas has been saved!\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)