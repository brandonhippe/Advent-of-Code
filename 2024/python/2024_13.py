from typing import List, Tuple, Any
import numpy as np
import re
from math import isclose


def gauss_jordan_elimination(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """ Gauss Jordan Elimination
    """
    n = len(b)
    ab = np.hstack((a, b.reshape(-1, 1)))

    for i in range(n):
        # Find the pivot
        pivot = ab[i, i]
        if pivot == 0:
            raise ValueError("Matrix is singular")

        # Normalize the row
        ab[i] /= pivot

        # Eliminate the other rows
        for j in range(n):
            if j == i:
                continue
            factor = ab[j, i]
            ab[j] -= factor * ab[i]

    # Return linear combination
    return ab[:, -1]


def part1(data: List[str]) -> Any:
    """ 2024 Day 13 Part 1
    >>> part1(["Button A: X+94, Y+34", "Button B: X+22, Y+67", "Prize: X=8400, Y=5400", "", "Button A: X+26, Y+66", "Button B: X+67, Y+21", "Prize: X=12748, Y=12176", "", "Button A: X+17, Y+86", "Button B: X+84, Y+37", "Prize: X=7870, Y=6450", "", "Button A: X+69, Y+23", "Button B: X+27, Y+71", "Prize: X=18641, Y=10279"])
    480
    """
    if data[-1] != '':
        data.append('')

    a, b, final_pos = None, None, None
    total_cost = 0
    for line in data:
        if len(line) == 0:
            # Calculate the linear combination
            combination = gauss_jordan_elimination(np.hstack((a.reshape(-1, 1), b.reshape(-1, 1))), final_pos)
            if all(isclose(round(c), c) for c in combination):
                total_cost += round(sum(m * c for m, c in zip((3, 1), combination)))

            continue

        if line.split(' ')[1] == 'A:':
            a = np.array([list(map(float, re.findall(r'-?\d+', line)))])
        elif line.split(' ')[1] == 'B:':
            b = np.array([list(map(float, re.findall(r'-?\d+', line)))])
        else:
            final_pos = np.array(list(map(float, re.findall(r'-?\d+', line))))

    return total_cost


def part2(data: List[str]) -> Any:
    """ 2024 Day 13 Part 2
    """

    if data[-1] != '':
        data.append('')

    a, b, final_pos = None, None, None
    total_cost = 0
    for line in data:
        if len(line) == 0:
            # Calculate the linear combination
            combination = gauss_jordan_elimination(np.hstack((a.reshape(-1, 1), b.reshape(-1, 1))), final_pos)
            if all(isclose(round(c), c, rel_tol=0, abs_tol=1e-9) for c in combination):
                total_cost += round(sum(m * c for m, c in zip((3, 1), combination)))

            continue

        if line.split(' ')[1] == 'A:':
            a = np.array([list(map(float, re.findall(r'-?\d+', line)))], dtype=np.float128)
        elif line.split(' ')[1] == 'B:':
            b = np.array([list(map(float, re.findall(r'-?\d+', line)))], dtype=np.float128)
        else:
            final_pos = np.array(list(map(float, re.findall(r'-?\d+', line))), dtype=np.float128)
            final_pos += 10_000_000_000_000

    return total_cost


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
        print(f"\nPart 1:\nNumber of tokens spent: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nNumber of tokens spent: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return (p1, p1_time.elapsed), (p2, p2_time.elapsed)


if __name__ == "__main__":
    main(True)
