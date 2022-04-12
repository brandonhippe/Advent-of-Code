import time
import re
import heapq

READING_ORDER = [[0, -1], [-1, 0], [1, 0], [0, 1]]

class Unit:
    def __init__(self, pos):
        self.hp = 200
        self.attack = 3
        self.pos = pos

    def __lt__(self, other):
        return self.pos[1] < other.pos[1] or (self.pos[1] == other.pos[1] and self.pos[0] < other.pos[0])

class Path:
    def __init__(self, path):
        self.path = path[:]
        self.pos = self.path[-1]
        self.d = len(self.path) - 1

    def __lt__(self, other):
        if self.d < other.d:
            return True

        if self.d > other.d:
            return False

        return self.path[1][1] < other.path[1][1] or (self.path[1][1] == other.path[1][1] and self.path[1][0] < other.path[1][0])

def manhatDist(p1, p2):
    return sum(abs(c1 - c2) for c1, c2 in zip(p1, p2))

def findNearest(unit, allies, enemies, walls):
    visited = []
    inQueue = [Path([unit.pos])]

    while len(inQueue) != 0:
        currPath = heapq.heappop(inQueue)
        if currPath.pos in [e.pos for e in enemies]:
            return [enemies[[e.pos for e in enemies].index(currPath.pos)], currPath.path[1]]

        for n in [[p + o for p, o in zip(currPath.pos, offset)] for offset in READING_ORDER]:
            if n in [v.pos for v in visited] or n in walls or n in [a.pos for a in allies]:
                continue

            heapq.heappush(inQueue, Path(currPath.path + [n]))
            
        visited.append(currPath)

    return [None] * 2

def iterate(walls, elfs, goblins):
    complete = True
    for x, y in [u.pos for u in sorted(elfs + goblins)]:            
        if [x, y] in [e.pos for e in elfs]:
            unit = elfs[[e.pos for e in elfs].index([x, y])]
            allies = elfs
            enemies = goblins
        elif [x, y] in [g.pos for g in goblins]:
            unit = goblins[[g.pos for g in goblins].index([x, y])]
            allies = goblins
            enemies = elfs
        else:
            continue

        if len(enemies) == 0:
            complete = False

        nearestEnemy, nextPos = findNearest(unit, allies, enemies, walls)

        if nearestEnemy is None:
            continue

        if nearestEnemy.pos != nextPos:
            # Moving
            unit.pos = nextPos[:]
        
        if manhatDist(unit.pos, nearestEnemy.pos) == 1:
            # Attacking
            nearestEnemy = None
            for n in [[p + o for p, o in zip(unit.pos, offset)] for offset in READING_ORDER]:
                try:
                    enemy = enemies[[e.pos for e in enemies].index(n)]
                    if nearestEnemy is None or enemy.hp < nearestEnemy.hp:
                        nearestEnemy = enemy
                except ValueError:
                    pass

            nearestEnemy.hp -= unit.attack
            if nearestEnemy.hp <= 0:
                enemies.pop(enemies.index(nearestEnemy))

    return complete
            
def printBattle(maxs, walls, elfs, goblins):
    for y in range(0, maxs[1] + 1):
        postStr = '   '
        for x in range(0, maxs[0] + 1):
            c = '.'
            if [x, y] in walls:
                c = '#'
            elif [x, y] in [e.pos for e in elfs]:
                c = 'E'
                postStr += f'E({elfs[[e.pos for e in elfs].index([x, y])].hp}), '
            elif [x, y] in [g.pos for g in goblins]:
                c = 'G'
                postStr += f'G({goblins[[g.pos for g in goblins].index([x, y])].hp}), '

            print(c, end='')
        print(f'{postStr[:-2]}')

def main(filename):
    testing = len(re.findall("\d+", filename)) > 0
    with open(filename, encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]
    
    walls = []
    elfs = []
    goblins = []
    maxs = [0, 0]
    for y, line in enumerate(lines):
        if y > maxs[1]:
            maxs[1] = y
        for x, l in enumerate(line):
            if x > maxs[0]:
                maxs[0] = x
            if l == '#':
                walls.append([x, y])
            elif l == 'E':
                elfs.append(Unit([x, y]))
            elif l == 'G':
                goblins.append(Unit([x, y]))
    
    rounds = 0
    while len(elfs) > 0 and len(goblins) > 0:
        if testing:
            print(f"\nAfter {rounds} Round{'s' if rounds != 1 else ''}:")
            printBattle(maxs, walls, elfs, goblins)

        if iterate(walls, elfs, goblins):
            rounds += 1

    if testing:
        print(f"\nAfter {rounds} Round{'s' if rounds != 1 else ''}:")
        printBattle(maxs, walls, elfs, goblins)

    winners = elfs[:] if len(goblins) == 0 else goblins[:]
    print(f"\nPart 1:\nCombat Outcome: {rounds * sum(w.hp for w in winners)}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input1.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
