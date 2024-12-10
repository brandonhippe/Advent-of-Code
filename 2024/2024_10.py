from typing import List, Tuple, Any
from collections import defaultdict, deque


def part1(data: List[str]) -> Any:
    """ 2024 Day 10 Part 1
    >>> part1(["89010123", "78121874", "87430965", "96549874", "45678903", "32019012", "01329801", "10456732"])
    36
    """

    heights = defaultdict(set)
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            heights[int(c)].add((x, y))

    score_sum = 0
    for pos in heights[0]:
        open_list = deque([(*pos, 0)])
        visited = set()
        finishes = set()
        while open_list:
            x, y, height = open_list.popleft()
            if height == 9:
                finishes.add((x, y))
                continue

            if (x, y) in visited:
                continue

            visited.add((x, y))

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_x, new_y = x + dx, y + dy
                if (new_x, new_y) in heights[height + 1]:
                    open_list.append((new_x, new_y, height + 1))

        score_sum += len(finishes)

    return score_sum


def part2(data: List[str]) -> Any:
    """ 2024 Day 10 Part 2
    >>> part2(["89010123", "78121874", "87430965", "96549874", "45678903", "32019012", "01329801", "10456732"])
    81
    """

    heights = defaultdict(set)
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            heights[int(c)].add((x, y))

    score_sum = 0
    for pos in heights[0]:
        open_list = deque([(*pos, 0)])
        visited = set()
        finishes = defaultdict(int)
        while open_list:
            x, y, height = open_list.popleft()
            if height == 9:
                finishes[(x, y)] += 1
                continue

            visited.add((x, y))

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_x, new_y = x + dx, y + dy
                if (new_x, new_y) in heights[height + 1]:
                    open_list.append((new_x, new_y, height + 1))

        score_sum += sum(finishes.values())

    return score_sum


def main(verbose: bool=False) -> Tuple[Tuple[Any, float]]:
    from pathlib import Path
    import sys, re
    sys.path.append(str(Path(__file__).parent.parent))
    from Modules.timer import Timer
    year, day = re.findall(r'\d+', str(__file__))[-2:]
    
    with open(Path(__file__).parent.parent / f"Inputs/{year}_{day}.txt", encoding='UTF-8') as f:
        data = [line.strip('\n') for line in f.readlines()]

    with Timer() as p1_time:
        p1 = part1(data)

    if verbose:
        print(f"\nPart 1:\nSum of trailhead scores: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nSum of trailhead ratings: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return (p1, p1_time.elapsed), (p2, p2_time.elapsed)


if __name__ == "__main__":
    main(True)
