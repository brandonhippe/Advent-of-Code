from typing import List, Tuple, Any
import re
from math import log10, isclose


class Robot:
    def __init__(self, init_str: str):
        self.x, self.y = (int(n) for n in re.search(r"p=(-?\d+),(-?\d+)", init_str).groups())
        self.xv, self.yv = (int(n) for n in re.search(r"v=(-?\d+),(-?\d+)", init_str).groups())

    def __repr__(self):
        return f"({self.x}, {self.y}) -> ({self.xv}, {self.yv})"
    
    def __hash__(self):
        return hash((self.x, self.y, self.xv, self.yv))
    
    def move(self, width: int, height: int):
        self.x += self.xv
        self.y += self.yv

        self.x %= width
        self.y %= height


def printRobots(positions: set[tuple[int,]], width: int, height: int):
    for y in range(height):
        for x in range(width):
            print('█' if (x, y) in positions else ' ', end='')
        print()


def part1(data: List[str], width: int=101, height: int=103) -> Any:
    """ 2024 Day 14 Part 1
    >>> part1(["p=0,4 v=3,-3", "p=6,3 v=-1,-3", "p=10,3 v=-1,2", "p=2,0 v=2,-1", "p=0,0 v=1,3", "p=3,0 v=-2,-2", "p=7,6 v=-1,-3", "p=3,0 v=-1,-2", "p=9,3 v=2,3", "p=7,3 v=-1,2", "p=2,4 v=2,-3", "p=9,5 v=-3,-3"], 11, 7)
    12
    """

    robots = [Robot(line) for line in data]
    for _ in range(100):
        for robot in robots:
            robot.move(width, height)


    quadrant_counts = [[0, 0], [0, 0]]
    for robot in robots:
        if robot.y == (height // 2) or robot.x == (width // 2):
            continue

        quadrant_counts[robot.y > (height // 2)][robot.x > (width // 2)] += 1

    return quadrant_counts[0][0] * quadrant_counts[1][1] * quadrant_counts[0][1] * quadrant_counts[1][0]


def part2(data: List[str], verbose: bool=False) -> Any:
    """ 2024 Day 14 Part 2
    """

    width, height = 101, 103
    robots = tuple(Robot(line) for line in data)
    seen = set()
    seconds = 0
    max_seconds = 0
    max_positions = set()
    max_amt_reflected = 0
    while robots not in seen:
        seconds += 1
        positions = set()
        seen.add(robots)
        for robot in robots:
            robot.move(width, height)
            positions.add((robot.x, robot.y))

        count = 0
        counted = set()
        for pos in positions:
            reflected_vert = ((width - pos[0] - 1) % width, pos[1])
            if pos not in counted and reflected_vert not in counted and reflected_vert in positions:
                counted.add(pos)
                counted.add(reflected_vert)
                count += 1

        if count > max_amt_reflected:
            max_amt_reflected = count
            max_seconds = seconds
            max_positions = positions
            # print(f"Seconds: {seconds}")
            # printRobots(positions, width, height)

        # if isclose(log10(seconds), log10(seconds) // 1):
        #     print(f"Seconds: {seconds}")

    if verbose:
        printRobots(max_positions, width, height)
    return max_seconds


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
        print(f"\nPart 1:\nSaftey Factor: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data, verbose)

    if verbose:
        print(f"\nPart 2:\nChristmas tree (above) appears after {p2} seconds\nRan in {p2_time.elapsed:0.4f} seconds")

    return (p1, p1_time.elapsed), (p2, p2_time.elapsed)


if __name__ == "__main__":
    main(True)
