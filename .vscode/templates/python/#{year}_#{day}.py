<<<<<<< HEAD
from typing import List, Tuple, Any


def part1(data: List[str]) -> Any:
    """ #{year} Day #{day} Part 1
    """

    return NotImplemented


def part2(data: List[str]) -> Any:
    """ #{year} Day #{day} Part 2
    """

    return NotImplemented


def main(verbose: bool=False) -> Tuple[Tuple[Any, float]]:
=======
def part1(data):
    """
    #{year} Day #{day} Part 1
    """

    return -1


def part2(data):
    """
    #{year} Day #{day} Part 2
    """

    return -1


def main(verbose = False):
>>>>>>> 39e116cf709a3434606ac8f4294a5d57736c0e8a
    from pathlib import Path
    import sys, re
    sys.path.append(str(Path(__file__).parent.parent))
    from Modules.timer import Timer
<<<<<<< HEAD
    year, day = re.findall(r'\d+', str(__file__))[-2:]
    
    with open(Path(__file__).parent.parent / f"Inputs/{year}_{day}.txt", encoding='UTF-8') as f:
        data = [line.strip('\n') for line in f.readlines()]

=======
    year, day = re.findall('\d+', str(Path(__file__)))
    
    with open(Path(__file__).parent.parent / f"Inputs/{year}_{day}.txt", encoding='UTF-8') as f:
        data = [line.strip('\n') for line in f.readlines()]
    
>>>>>>> 39e116cf709a3434606ac8f4294a5d57736c0e8a
    with Timer() as p1_time:
        p1 = part1(data)

    if verbose:
<<<<<<< HEAD
        print(f"\nPart 1:\n {p1}\nRan in {p1_time.elapsed:0.4f} seconds")
=======
        print(f"\nPart 1:\n{p1}\nRan in {p1_time.elapsed:0.4f} seconds")
>>>>>>> 39e116cf709a3434606ac8f4294a5d57736c0e8a

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
<<<<<<< HEAD
        print(f"\nPart 2:\n {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return (p1, p1_time.elapsed), (p2, p2_time.elapsed)
=======
        print(f"\nPart 2:\n{p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]
>>>>>>> 39e116cf709a3434606ac8f4294a5d57736c0e8a


if __name__ == "__main__":
    main(True)
