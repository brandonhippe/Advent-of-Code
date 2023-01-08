import time
import re
import copy

class Particle:
    def __init__(self, nums, ix):
        self.pos = nums[:3]
        self.vel = nums[3:6]
        self.acc = nums[6:]
        self.ix = ix

    def update(self):
        self.vel = [v + a for v, a in zip(self.vel, self.acc)]
        self.pos = [p + v for p, v in zip(self.pos, self.vel)]

def manhatDist(p1, p2):
    return sum([abs(c1 - c2) for c1, c2 in zip(p1, p2)])

def closestParticle(particles):
    minD = float('inf')
    for p in particles:
        d = manhatDist(p.pos, (0, 0, 0))
        if d < minD:
            minD = d
            minP = p

    return minP

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        particles = [Particle([int(x) for x in re.findall('-?\d+', line)], i) for i, line in enumerate(f.readlines())]

    particlesP2 = copy.deepcopy(particles)

    closest = particles[particles.index(closestParticle(particles)) - 1]
    i = 0
    while i % 1000 != 0 or closest != closestParticle(particles):
        closest = closestParticle(particles)
        for p in particles:
            p.update()

        i += 1

    part1 = closest.ix

    particles = particlesP2
    pLen = len(particles) + 1
    i = 0

    while i % 1000 != 0 or len(particles) != pLen:
        pLen = len(particles)
        poses = set()
        deleting = set()

        for p in particles:
            p.update()

            if tuple(p.pos) in poses:
                poses.remove(tuple(p.pos))
                deleting.add(tuple(p.pos))
            elif tuple(p.pos) not in deleting:
                poses.add(tuple(p.pos))

        newParticles = []
        for p in particles:
            if tuple(p.pos) not in deleting:
                newParticles.append(p)

        particles = newParticles
        i += 1

    if verbose:
        print(f"\nPart 1:\nManhattan distance to closest particle: {part1}\n\nPart 2:\nNumber of particles after resolving collisions: {len(particles)}")

    return [part1, len(particles)]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
    