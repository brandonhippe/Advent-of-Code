import time
import re

class Reindeer:
    def __init__(self, text):
        self.name = text.split(' ')[0]
        self.speed, self.duration, self.rest = [int(x) for x in re.findall('\d+', text)]

    def distance(self, time):
        d = 0
        while time >= self.duration:
            d += self.speed * self.duration
            time -= self.duration + self.rest

        if time < 0:
            time = 0

        return d + self.speed * time

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        deers = [Reindeer(line) for line in f.readlines()]

    part1 = max(r.distance(2503) for r in deers)

    points = {r.name: 0 for r in deers}
    for t in range(1, 2504):
        best = float('-inf')
        winner = None
        for r in deers:
            d = r.distance(t)
            if d > best:
                best = d
                winner = r.name

        points[winner] += 1

    part2 = max(points.values())

    if verbose:
        print(f"\nPart 1:\nDistance of winning Reindeer: {part1}\n\nPart 2:\nMost points: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
