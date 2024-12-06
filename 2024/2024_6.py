from typing import List, Tuple, Set, Generator, Any


def parse_input(data: List[str]) -> Tuple[Tuple[int,], Tuple[int,], Set[Tuple[int,]]]:
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
    return pos, curr_dir, walls


def guard_movement(pos: Tuple[int,], curr_dir: Tuple[int,], walls: Set[Tuple[int,]], dims: Tuple[int,]) -> Generator[Tuple[Tuple[int,],], None, None]:
    while all(0 <= pos[i] < dims[i] for i in range(len(dims))):
        yield pos, curr_dir
        while True:
            next_pos = tuple(map(sum, zip(pos, curr_dir)))
            if next_pos not in walls:
                pos = next_pos
                break

            curr_dir = -curr_dir[1], curr_dir[0]


def part1(data: List[str]) -> Any:
    """ 2024 Day 6 Part 1
    >>> part1(["....#.....", ".........#", "..........", "..#.......", ".......#..", "..........", ".#..^.....", "........#.", "#.........", "......#..."])
    41
    """
    pos, curr_dir, walls = parse_input(data)
    return len(set(g[0] for g in guard_movement(pos, curr_dir, walls, (len(data[0]), len(data)))))



def part2(data: List[str]) -> Any:
    """ 2024 Day 6 Part 2
    >>> part2(["....#.....", ".........#", "..........", "..#.......", ".......#..", "..........", ".#..^.....", "........#.", "#.........", "......#..."])
    6
    """
    def makes_loop(pos: Tuple[int, int], curr_dir: Tuple[int, int], visited: Set[Tuple[int,]]) -> bool:
        for curr_pos, curr_dir in guard_movement(pos, curr_dir, walls, (len(data[0]), len(data))):
            if (*curr_pos, *curr_dir) in visited:
                return True
            
            visited.add((*curr_pos, *curr_dir))
        
        return False

    start_pos, start_dir, walls = parse_input(data)
    obstructions = set()
    checked = {start_pos}
    visited_dirs = set()

    for curr_pos, curr_dir in guard_movement(start_pos[:], start_dir[:], walls, (len(data[0]), len(data))):
        if not (curr_pos == start_pos and curr_dir == start_dir and len(visited_dirs) == 0):
            visited_dirs.add((*curr_pos, *curr_dir))

        if curr_pos in checked or len(visited_dirs) == 0:
            continue

        checked.add(curr_pos)

        walls.add(curr_pos)
        if makes_loop(tuple(p - d for p, d in zip(curr_pos, curr_dir)), (-curr_dir[1], curr_dir[0]), visited_dirs.copy()):
            obstructions.add(curr_pos)

        walls.remove(curr_pos)

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
