import time
import re

class Group:
    def __init__(self, army, groupText):
        self.army = army
        self.units, self.hp, self.damage, self.initiative = (int(x) for x in re.findall('\d+', groupText))
        self.damageType = groupText.split(f'{self.damage} ')[-1].split(' damage')[0]

        self.weak = []
        self.immune = []

        if '(' in groupText:
            specials = re.split(' to |; ', re.findall('\(.*\)', groupText)[0][1:-1])
            for i, s in enumerate(specials):
                if s not in ['weak', 'immune']:
                    if specials[i - 1] == 'weak':
                        self.weak = s.split(', ')
                    else:
                        self.immune = s.split(', ')

        self.attacking = None
        self.defending = None

    def __gt__(self, other):
        return self.units * self.damage > other.units * other.damage or (self.units * self.damage == other.units * other.damage and self.initiative > other.initiative)

    def damageDealt(self, other):
        return self.units * self.damage * (0 if self.damageType in other.immune else 1) * (2 if self.damageType in other.weak else 1)

    def takeDamage(self):
        if self.defending.units > 0:
            dam = self.defending.damageDealt(self)
            self.units -= dam // self.hp

def targetPhase(groups):
    groups = sorted(groups, reverse=True)
    
    for g in groups:
        most = 0
        chosen = None
        for gr in groups:
            if gr.defending is None and gr.army != g.army:
                dam = g.damageDealt(gr)
                if dam > most or (dam == most and (chosen is None or gr.initiative < chosen.initiative)):
                    most = g.damageDealt(gr)
                    chosen = gr

        if chosen:
            g.attacking = chosen
            chosen.defending = g

def attackingPhase(groups):
    groups = sorted(groups, reverse=True, key=lambda g: g.initiative)

    newGroups = []
    for g in groups:
        if g.attacking is not None:
            g.attacking.takeDamage()
            if g.attacking.units > 0:
                newGroups.append(g.attacking)

        if g.defending is None:
            newGroups.append(g)

    return newGroups

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    groups = []
    for line in lines:
        if len(line) == 0:
            continue

        if line[-1] == ':':
            army = line[:-1]
        else:
            groups.append(Group(army, line))

    while len({g.army for g in groups}) != 1:
        targetPhase(groups)
        groups = attackingPhase(groups)
        for g in groups:
            g.attacking = None
            g.defending = None

    print(f"\nPart 1:\nTotal remaining units of winning army: {sum([g.units for g in groups])}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
