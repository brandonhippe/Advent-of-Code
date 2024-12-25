from typing import List, Tuple, Any
import re


def part1(data: List[str]) -> Any:
    """ 2024 Day 3 Part 1
    >>> part1(["xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"])
    161
    """
    count = 0
    for line in data:
        for match in re.findall(r'mul\((\d+),(\d+)\)', line):
            count += int(match[0]) * int(match[1])

    return count


def part2(data: List[str]) -> Any:
    """ 2024 Day 3 Part 2
    >>> part2(["xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"])
    48
    """
    count = 0
    enabled = True
    for line in data:
        for match in re.findall(r"(mul\((\d+),(\d+)\))|(do\(\))|(don't\(\))", line):
            if len(match[1]) and len(match[2]):
                count += int(match[1]) * int(match[2]) * enabled
            elif len(match[3]):
                enabled = True
            elif len(match[4]):
                enabled = False
            else:
                raise ValueError("Invalid match")

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
        print(f"\nPart 1:\nSum of multiplication instructions: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nSum of enabled multiplication instructions: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return (p1, p1_time.elapsed), (p2, p2_time.elapsed)


if __name__ == "__main__":
    main(True)