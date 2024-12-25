from typing import List, Tuple, Any
import numpy as np


def check_valid(diffs: List[int]) -> bool:
    """ Check if a list of differences is valid
    """
    return all(1 <= d <= 3 for d in diffs) or all(-3 <= d <= -1 for d in diffs)


def part1(data: List[str]) -> Any:
    """ 2024 Day 2 Part 1
    >>> part1(["7 6 4 2 1", "1 2 7 8 9", "9 7 6 2 1", "1 3 2 4 5", "8 6 4 4 1", "1 3 6 7 9"])
    2
    """

    return sum(check_valid(np.diff([int(x) for x in line.split()])) for line in data)


def part2(data: List[str]) -> Any:
    """ 2024 Day 2 Part 2
    >>> part2(["7 6 4 2 1", "1 2 7 8 9", "9 7 6 2 1", "1 3 2 4 5", "8 6 4 4 1", "1 3 6 7 9"])
    4
    """
    count = 0
    for line in data:
        base_nums = [int(x) for x in line.split()]
        diffs = np.diff(base_nums)
        if check_valid(diffs):
            count += 1
            continue
        
        for ix in range(len(base_nums)):
            nums = base_nums[:ix] + base_nums[ix+1:]
            
            diffs = np.diff(nums)
            if check_valid(diffs):
                count += 1
                break

    return count


def main(verbose: bool=False) -> Tuple[Tuple[Any, float]]:
    from pathlib import Path
    import sys, re
    sys.path.append(str(Path(__file__).parent.parent.parent))
    from Modules.timer import Timer
    year, day = re.findall(r'\d+', str(__file__))[-2:]
    
    with open(Path(__file__).parent.parent.parent / f"Inputs/{year}_{day}.txt", encoding='UTF-8') as f:
        data = [line.strip('\n') for line in f.readlines()]

    with Timer() as p1_time:
        p1 = part1(data)

    if verbose:
        print(f"\nPart 1:\nValid count: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nValid count: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return (p1, p1_time.elapsed), (p2, p2_time.elapsed)


if __name__ == "__main__":
    main(True)