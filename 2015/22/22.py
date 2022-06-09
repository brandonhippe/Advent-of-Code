import time
import re

def applyEffects(hp, mana, boss_hp, effects):
    newEffects = []
    armor = 0
    for e, timer in effects:
        if e == "Shield":
            armor += 7
        elif e == "Poison":
            boss_hp -= 3
        elif e == "Recharge":
            mana += 101

        timer -= 1
        if timer > 0:
            newEffects.append([e, timer])

    return [hp, mana, armor, boss_hp, newEffects]

def simulateP1(you, boss, effects):
    hp, mana = you
    boss_hp, boss_damage = boss

    if min(hp, boss_hp) <= 0 or mana < 53:
        return 0 if boss_hp <= 0 else float('inf')

    bestCost = float('inf')
    for e in ["Magic Missile", "Drain", "Shield", "Poison", "Recharge"]:
        new_hp, new_mana, new_armor, new_boss_hp, newEffects = applyEffects(hp, mana, boss_hp, effects)
        cost = 0
        if e == "Magic Missile" and new_mana >= 53:
            new_boss_hp -= 4
            new_mana -= 53
            cost = 53
        elif e == "Drain" and new_mana >= 73:
            new_boss_hp -= 2
            new_hp += 2
            new_mana -= 73
            cost = 73
        elif e == "Shield" and new_mana >= 113 and "Shield" not in [effect[0] for effect in newEffects]:
            newEffects.append(["Shield", 6])
            new_mana -= 113
            cost = 113
        elif e == "Poison" and new_mana >= 173 and "Poison" not in [effect[0] for effect in newEffects]:
            newEffects.append(["Poison", 6])
            new_mana -= 173
            cost = 173
        elif e == "Recharge" and new_mana >= 229 and "Recharge" not in [effect[0] for effect in newEffects]:
            newEffects.append(["Recharge", 5])
            new_mana -= 229
            cost = 229
        else:
            continue 

        if min(new_hp, new_boss_hp) > 0:
            new_hp, new_mana, new_armor, new_boss_hp, newEffects = applyEffects(new_hp, new_mana, new_boss_hp, newEffects)

        if min(new_hp, new_boss_hp) > 0:
            new_hp -= max(1, boss_damage - new_armor)

        cost += simulateP1([new_hp, new_mana], [new_boss_hp, boss_damage], newEffects)
        if cost < bestCost:
            bestCost = cost

    return bestCost

def simulateP2(you, boss, effects):
    hp, mana = you
    boss_hp, boss_damage = boss

    if min(hp, boss_hp) <= 0 or mana < 53:
        return 0 if boss_hp <= 0 else float('inf')

    bestCost = float('inf')
    for e in ["Magic Missile", "Drain", "Shield", "Poison", "Recharge"]:
        new_hp, new_mana, new_armor, new_boss_hp, newEffects = applyEffects(hp, mana, boss_hp, effects)
        cost = 0
        if e == "Magic Missile" and new_mana >= 53:
            new_boss_hp -= 4
            new_mana -= 53
            cost = 53
        elif e == "Drain" and new_mana >= 73:
            new_boss_hp -= 2
            new_hp += 2
            new_mana -= 73
            cost = 73
        elif e == "Shield" and new_mana >= 113 and "Shield" not in [effect[0] for effect in newEffects]:
            newEffects.append(["Shield", 6])
            new_mana -= 113
            cost = 113
        elif e == "Poison" and new_mana >= 173 and "Poison" not in [effect[0] for effect in newEffects]:
            newEffects.append(["Poison", 6])
            new_mana -= 173
            cost = 173
        elif e == "Recharge" and new_mana >= 229 and "Recharge" not in [effect[0] for effect in newEffects]:
            newEffects.append(["Recharge", 5])
            new_mana -= 229
            cost = 229
        else:
            continue 

        if min(new_hp, new_boss_hp) > 0:
            new_hp, new_mana, new_armor, new_boss_hp, newEffects = applyEffects(new_hp, new_mana, new_boss_hp, newEffects)

        if min(new_hp, new_boss_hp) > 0:
            new_hp -= max(1, boss_damage - new_armor)

        cost += simulateP2([new_hp - 1, new_mana], [new_boss_hp, boss_damage], newEffects)
        if cost < bestCost:
            bestCost = cost

    return bestCost

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        boss_hp, boss_damage = [[int(x) for x in re.findall('\d+', line)][0] for line in f.readlines()]

    print(f"\nPart 1:\nLeast mana to win: {simulateP1([50, 500], [boss_hp, boss_damage], [])}")
    print(f"\nPart 2:\nLeast mana to win on hard: {simulateP2([50, 500], [boss_hp, boss_damage], [])}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
