from typing import Any, List, Tuple
from collections import defaultdict, deque
from itertools import product


def part1(data: List[str]) -> Any:
    """
    2024 Day 23 Part 1
    >>> part1(["kh-tc", "qp-kh", "de-cg", "ka-co", "yn-aq", "qp-ub", "cg-tb", "vc-aq", "tb-ka", "wh-tc", "yn-cg", "kh-ub", "ta-co", "de-co", "tc-td", "tb-wq", "wh-td", "ta-ka", "td-qp", "aq-cg", "wq-ub", "ub-vc", "de-ta", "wq-aq", "wq-vc", "wh-yn", "ka-de", "kh-ta", "co-tc", "wh-qp", "tb-vc", "td-yn"])
    7
    """
    connections = defaultdict(set)
    for line in data:
        a, b = line.split("-")
        connections[a].add(b)
        connections[b].add(a)

    total = set()
    for k, connected in connections.items():
        if k[0] != 't':
            continue

        for k1 in connected:
            for k2 in connections[k1]:
                if k2 in connected:
                    total.add(tuple(sorted([k, k1, k2])))

    return len(total)


def part2(data: List[str]) -> Any:
    """
    2024 Day 23 Part 2
    >>> part2(["kh-tc", "qp-kh", "de-cg", "ka-co", "yn-aq", "qp-ub", "cg-tb", "vc-aq", "tb-ka", "wh-tc", "yn-cg", "kh-ub", "ta-co", "de-co", "tc-td", "tb-wq", "wh-td", "ta-ka", "td-qp", "aq-cg", "wq-ub", "ub-vc", "de-ta", "wq-aq", "wq-vc", "wh-yn", "ka-de", "kh-ta", "co-tc", "wh-qp", "tb-vc", "td-yn"])
    'co,de,ka,ta'
    """
    def all_connected(lan_party):
        return all(k1 in connections[k2] or k1 == k2 for k1, k2 in product(lan_party, lan_party))
    
    connections = defaultdict(set)
    for line in data:
        a, b = line.split("-")
        connections[a].add(b)
        connections[b].add(a)

    lan_party = set()
    open_list = deque([{k} for k in connections.keys()])
    open_set = {tuple(sorted(k)) for k in open_list}
    visited = set()

    while open_list:
        current = open_list.popleft()
        if tuple(sorted(current)) in visited:
            continue
        
        visited.add(tuple(sorted(current)))
        if len(current) > len(lan_party) and all_connected(current):
            lan_party = current

        available = set(connections.keys())
        for k in current:
            available &= connections[k]

        for k in available:
            new_lan_party = current | {k}
            if tuple(sorted(new_lan_party)) not in open_set:
                open_set.add(tuple(sorted(new_lan_party)))
                open_list.append(new_lan_party)

    return ",".join(sorted(lan_party))


def main(verbose: bool = False) -> Tuple[Tuple[Any, float]]:
    import re
    import sys
    from pathlib import Path

    sys.path.append(str(Path(__file__).parent.parent))
    from Modules.timer import Timer

    year, day = re.findall(r"\d+", str(__file__))[-2:]

    with open(
        Path(__file__).parent.parent / f"Inputs/{year}_{day}.txt", encoding="UTF-8"
    ) as f:
        data = [line.strip("\n") for line in f.readlines()]

    with Timer() as p1_time:
        p1 = part1(data)

    if verbose:
        print(f"\nPart 1:\nGroups of 3 interconnected pcs with one starting with t: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nLargest fully connected group: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return (p1, p1_time.elapsed), (p2, p2_time.elapsed)


if __name__ == "__main__":
    main(True)
