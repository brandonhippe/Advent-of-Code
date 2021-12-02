class passport:
    def __init__(self, data):
        data = data.replace('\n', ' ')
        words = data.split(' ')

        for word in words:
            d = word.split(':')
            if len(d) > 1:
                setattr(self, d[0], d[1])
    
    def p1_valid(self):
        if hasattr(self, 'byr') and hasattr(self, 'iyr') and hasattr(self, 'eyr') and hasattr(self, 'hgt') and hasattr(self, 'hcl') and hasattr(self, 'ecl') and hasattr(self, 'pid'):
            return 1

        return 0

    def p2_valid(self):
        if not (hasattr(self, 'byr') and hasattr(self, 'iyr') and hasattr(self, 'eyr') and hasattr(self, 'hgt') and hasattr(self, 'hcl') and hasattr(self, 'ecl') and hasattr(self, 'pid')):
            return 0

        for a in dir(self):
            if not a.startswith('__'):
                value = getattr(self, a)
                if a == 'byr':
                    if value.isnumeric():
                        value = int(value)
                        if not (value >= 1920 and value <= 2002):
                            return 0
                    else:
                        return 0
                elif a == 'iyr':
                    if value.isnumeric():
                        value = int(value)
                        if not (value >= 2010 and value <= 2020):
                            return 0
                    else:
                        return 0
                elif a == 'eyr':
                    if value.isnumeric():
                        value = int(value)
                        if not (value >= 2020 and value <= 2030):
                            return 0
                    else:
                        return 0
                elif a == 'hgt':
                    num = value[:-2:]
                    unit = value[-2:]
                    if num.isnumeric():
                        num = int(num)
                    else:
                        return 0

                    if unit == 'cm':
                        if not (num >= 150 and num <= 193):
                            return 0
                    elif unit == 'in':
                        if not (num >= 59 and num <= 76):
                            return 0
                    else:
                        return 0
                elif a == 'hcl':
                    if value[0] == '#' and len(value) == 7:
                        value = value[1:]
                        for c in value:
                            if (not c >= '0' and c <= '9') and (not c >= 'a' and c <= 'z') and (not c >= 'A' and c <= 'Z'):
                                return 0
                    else:
                        return 0
                elif a == 'ecl':
                    if not (value == 'amb' or value == 'blu' or value == 'brn' or value == 'gry' or value == 'grn' or value == 'hzl' or value == 'oth'):
                        return 0
                elif a == 'pid':
                    if value.isnumeric():
                        if not len(value) == 9:
                            return 0
                    else:
                        return 0

        return 1

    def printPassport(self):
        print('\n')
        for a in dir(self):
            if '_' not in a:
                print(a + ': ' + getattr(self, a))

        print('\n')    
            

def main():
    with open('input.txt', encoding='UTF-8') as f:
        lines = f.readlines()


    passports = []
    string = ""

    for line in lines:
        if len(line) > 1:
            string = string + line
        else:
            passports.append(passport(string))
            string = ""

    count = 0
    for p in passports:
        count += p.p1_valid()

    print("Part 1\nValid: " + str(count) + "\n")

    count = 0
    for p in passports:
        count += p.p2_valid()

    print("Part 2\nValid: " + str(count) + "\n")


main()
