import time
import re

def simulate(you, boss):
    hp, damage, armor = you
    boss_hp, boss_damage, boss_armor = boss

    while min(hp, boss_hp) > 0:
        boss_hp -= max(1, damage - boss_armor)
        if boss_hp <= 0:
            break

        hp -= max(1, boss_damage - armor)

    return hp > 0

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    boss_hp, boss_damage, boss_armor = [[int(x) for x in re.findall('\d+', line)][0] for line in lines[:3]]
    
    shop = {"Weapons:": {}, "Armor:": {}, "Rings:": {}}
    for line in lines[4:]:
        if len(line) == 0:
            continue

        line = re.split('\s\s+', line)
        if ':' in line[0]:
            current = line[0]
        else:
            shop[current][line[0]] = [int(x) for x in line[1:]]

    cheapest = float('inf')
    expensive = float('-inf')
    for w in list(shop["Weapons:"].keys()):
        for a in list(shop["Armor:"].keys()) + [None]:
            for r1 in list(shop["Rings:"].keys()) + [None]:
                for r2 in list(shop["Rings:"].keys()) + [None]:
                    if r1 == r2:
                        continue
                    
                    cost, damage, armor = [shop["Weapons:"][w][i] + (shop["Armor:"][a][i] if a is not None else 0) + (shop["Rings:"][r1][i] if r1 is not None else 0) + (shop["Rings:"][r2][i] if r2 is not None else 0) for i in range (3)]
                    if cost < cheapest and simulate([100, damage, armor], [boss_hp, boss_damage, boss_armor]):
                        cheapest = cost

                    if cost > expensive and not simulate([100, damage, armor], [boss_hp, boss_damage, boss_armor]):
                        expensive = cost

    print(f"\nPart 1:\nCheapest equipment to win: {cheapest}")
    print(f"\nPart 2:\nMost expensive equipment to lose: {expensive}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
