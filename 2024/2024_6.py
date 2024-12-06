from typing import List, Tuple, Any
from itertools import product


def part1(data: List[str]) -> Any:
    """ 2024 Day 6 Part 1
    >>> part1(["....#.....", ".........#", "..........", "..#.......", ".......#..", "..........", ".#..^.....", "........#.", "#.........", "......#..."])
    41
    """

    walls = set()
    pos = None
    curr_dir = None
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char == '#':
                walls.add((x, y))
            elif char != '.':
                pos = (x, y)
                curr_dir = {'^': (0, -1), 'v': (0, 1), '<': (-1, 0), '>': (1, 0)}[char]

    assert pos is not None and curr_dir is not None, "No starting position found"

    visited = set()
    while 0 <= pos[0] < len(data[0]) and 0 <= pos[1] < len(data):
        visited.add(pos)
        while True:
            next_pos = tuple(map(sum, zip(pos, curr_dir)))
            if next_pos not in walls:
                pos = next_pos
                break

            curr_dir = -curr_dir[1], curr_dir[0]

    return len(visited)


def part2(data: List[str]) -> Any:
    """ 2024 Day 6 Part 2
    >>> part2(["....#.....", ".........#", "..........", "..#.......", ".......#..", "..........", ".#..^.....", "........#.", "#.........", "......#..."])
    6
    """
    def makes_loop(pos: Tuple[int, int], curr_dir: Tuple[int, int]) -> bool:
        visited = set()
        while 0 <= pos[0] < len(data[0]) and 0 <= pos[1] < len(data):
            if (*pos, *curr_dir) in visited:
                return True
            
            visited.add((*pos, *curr_dir))
            while True:
                next_pos = tuple(map(sum, zip(pos, curr_dir)))
                if next_pos not in walls:
                    pos = next_pos
                    break

                curr_dir = -curr_dir[1], curr_dir[0]

        return False
    
    def check_right(pos: Tuple[int, int], curr_dir: Tuple[int, int]) -> bool:
        same_ix = curr_dir.index(0) 
        for wall in walls:
            dist = wall[1 - same_ix] - pos[1 - same_ix]
            if wall[same_ix] == pos[same_ix] and abs(dist) // dist == curr_dir[1 - same_ix]:
                return True
            
        return False

    walls = set()
    start_pos = None
    start_dir = None
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char == '#':
                walls.add((x, y))
            elif char != '.':
                start_pos = (x, y)
                start_dir = {'^': (0, -1), 'v': (0, 1), '<': (-1, 0), '>': (1, 0)}[char]

    assert start_pos is not None and start_dir is not None, "No starting position found"

    obstructions = set()
    pos = start_pos[:]
    curr_dir = start_dir[:]
    while 0 <= pos[0] < len(data[0]) and 0 <= pos[1] < len(data):
        while True:
            next_pos = tuple(map(sum, zip(pos, curr_dir)))
            if next_pos not in walls:
                if check_right(pos, (-curr_dir[1], curr_dir[0])):
                    walls.add(next_pos)
                    if makes_loop(start_pos[:], start_dir[:]):
                        obstructions.add(next_pos)
                    walls.remove(next_pos)

                pos = next_pos
                break

            curr_dir = -curr_dir[1], curr_dir[0]
    
    return len(obstructions)


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
        print(f"\nPart 1:\nNumber of positions visited: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nNumber of obstacle positions that make a loop: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return (p1, p1_time.elapsed), (p2, p2_time.elapsed)


if __name__ == "__main__":
    main(True)
