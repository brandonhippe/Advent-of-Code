from collections import defaultdict


def part1(data):
    """ 2020 Day 24 Part 1

    >>> part1(['sesenwnenenewseeswwswswwnenewsewsw', 'neeenesenwnwwswnenewnwwsewnenwseswesw', 'seswneswswsenwwnwse', 'nwnwneseeswswnenewneswwnewseswneseene', 'swweswneswnenwsewnwneneseenw', 'eesenwseswswnenwswnwnwsewwnwsene', 'sewnenenenesenwsewnenwwwse', 'wenwwweseeeweswwwnwwe', 'wsweesenenewnwwnwsenewsenwwsesesenwne', 'neeswseenwwswnwswswnw', 'nenwswwsewswnenenewsenwsenwnesesenew', 'enewnwewneswsewnwswenweswnenwsenwsw', 'sweneswneswneneenwnewenewwneswswnese', 'swwesenesewenwneswnwwneseswwne', 'enesenwswwswneneswsenwnewswseenwsese', 'wnwnesenesenenwwnenwsewesewsesesew', 'nenewswnwewswnenesenwnesewesw', 'eneswnwswnwsenenwnwnwwseeswneewsenese', 'neswnwewnwnwseenwseesewsenwsweewe', 'wseweeenwnesenwwwswnew'])
    10
    """

    floorTiles = set()

    for line in data:
        loc = (0, 0)
        pChar = 'e'
        for l in line:
            if l == 'e':
                if pChar != 's':
                    loc = (loc[0] + 1, loc[1])
            elif l == 'w':
                if pChar != 'n':
                    loc = (loc[0] - 1, loc[1])
            elif l == 'n':
                loc = (loc[0], loc[1] - 1)
            elif l == 's':
                loc = (loc[0], loc[1] + 1)
            
            pChar = l
        
        if loc in floorTiles:
            floorTiles.remove(loc)
        else:
            floorTiles.add(loc)
    
    return len(floorTiles)


def part2(data):
    """ 2020 Day 24 Part 2

    >>> part2(['sesenwnenenewseeswwswswwnenewsewsw', 'neeenesenwnwwswnenewnwwsewnenwseswesw', 'seswneswswsenwwnwse', 'nwnwneseeswswnenewneswwnewseswneseene', 'swweswneswnenwsewnwneneseenw', 'eesenwseswswnenwswnwnwsewwnwsene', 'sewnenenenesenwsewnenwwwse', 'wenwwweseeeweswwwnwwe', 'wsweesenenewnwwnwsenewsenwwsesesenwne', 'neeswseenwwswnwswswnw', 'nenwswwsewswnenenewsenwsenwnesesenew', 'enewnwewneswsewnwswenweswnenwsenwsw', 'sweneswneswneneenwnewenewwneswswnese', 'swwesenesewenwneswnwwneseswwne', 'enesenwswwswneneswsenwnewswseenwsese', 'wnwnesenesenenwwnenwsewesewsesesew', 'nenewswnwewswnenesenwnesewesw', 'eneswnwswnwsenenwnwnwwseeswneewsenese', 'neswnwewnwnwseenwseesewsenwsweewe', 'wseweeenwnesenwwwswnew'])
    2208
    """

    floorTiles = set()

    for line in data:
        loc = (0, 0)
        pChar = 'e'
        for l in line:
            if l == 'e':
                if pChar != 's':
                    loc = (loc[0] + 1, loc[1])
            elif l == 'w':
                if pChar != 'n':
                    loc = (loc[0] - 1, loc[1])
            elif l == 'n':
                loc = (loc[0], loc[1] - 1)
            elif l == 's':
                loc = (loc[0], loc[1] + 1)
            
            pChar = l
        
        if loc in floorTiles:
            floorTiles.remove(loc)
        else:
            floorTiles.add(loc)
    
    for _ in range(100):
        floorTiles = iterate(floorTiles)

    return len(floorTiles)


def iterate(tiles):
    newTiles = defaultdict(lambda: 0)
    for t in list(tiles):
        for nOff in [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]:
            newTiles[tuple(p + o for p, o in zip(t, nOff))] += 1

    return set(k for k, v in zip(newTiles.keys(), newTiles.values()) if v == 2 or (k in tiles and v == 1))


def main(verbose = False):
    from pathlib import Path
    import sys, re
    sys.path.append(str(Path(__file__).parent.parent))
    from Modules.timer import Timer
    year, day = re.findall('\d+', str(__file__))[-2:]
    
    with open(Path(__file__).parent.parent / f"Inputs/{year}_{day}.txt", encoding='UTF-8') as f:
        data = [line.strip('\n') for line in f.readlines()]

    with Timer() as p1_time:
        p1 = part1(data)

    if verbose:
        print(f"\nPart 1:\nNumber of tiles with black side up: {p1}\nRan in {p1_time.elapsed:0.4f} seconds")

    with Timer() as p2_time:
        p2 = part2(data)

    if verbose:
        print(f"\nPart 2:\nNumber of tiles with black side up after 100 days: {p2}\nRan in {p2_time.elapsed:0.4f} seconds")

    return [(p1, p1_time.elapsed), (p2, p2_time.elapsed)]


if __name__ == "__main__":
    main(True)