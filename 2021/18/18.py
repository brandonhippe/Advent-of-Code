import time

class snailFishNumber:
    def __init__(self, text, parent=0):
        self.regularNumber = False
        self.parent = parent

        if text[0] != '[':
            self.regularNumber = True
            self.value = int(text)
        else:
            tempText = text[1:-1]
            
            lText = ''
            i = 0
            opened = 0
            while True:
                if tempText[i] == '[':
                    opened += 1
                elif tempText[i] == ']':
                    opened -= 1
                elif tempText[i] == ',' and opened == 0:
                    break

                lText += tempText[i]
                i += 1

            rText = tempText[i + 1:]

            self.children = [snailFishNumber(lText, self), snailFishNumber(rText, self)]
    
    def reduction(self):
        changed = True
        while changed:
            changed = False
            changed = self.explode(0)
            if changed:
                continue
            changed = self.split()

    def explode(self, nested):
        if self.regularNumber:
            return False
        elif nested == 4:
            self.parent.insertLeft(self.children[0].value, self)
            self.parent.insertRight(self.children[1].value, self)
            return True
        
        for (i, child) in enumerate(self.children):
            tempReturn = child.explode(nested + 1)
            if tempReturn:
                if nested == 3:
                    self.children[i] = snailFishNumber('0', self)

                return True
        
        return False

    def insertLeft(self, num, child=0):
        if self.regularNumber:
            self.value += num
            return
        
        if child == 0:
            self.children[1].insertLeft(num)
        else:
            if self.children[0] == child:
                if self.parent != 0:
                    self.parent.insertLeft(num, self)
            else:
                self.children[0].insertLeft(num)

    def insertRight(self, num, child=0):
        if self.regularNumber:
            self.value += num
            return
        
        if child == 0:
            self.children[0].insertRight(num)
        else:
            if self.children[1] == child:
                if self.parent != 0:
                    self.parent.insertRight(num, self)
            else:
                self.children[1].insertRight(num)

    def split(self):
        if self.regularNumber:
            if self.value >= 10:
                self.regularNumber = False
                self.children = [snailFishNumber(str(self.value // 2), self), snailFishNumber(str((self.value + 1) // 2), self)]
                return True
        else:
            for child in self.children:
                tempReturn = child.split()
                if tempReturn:
                    return True
            
        return False

    def numberString(self):
        if self.regularNumber:
            return str(self.value)
        else:
            return '[' + self.children[0].numberString() + ',' + self.children[1].numberString() + ']'

    def magnitude(self):
        if self.regularNumber:
            return self.value
        else:
            return (3 * self.children[0].magnitude()) + (2 * self.children[1].magnitude())

def main(verbose):
    with open('input.txt', encoding='UTF-8') as f:
        lines = [line.strip() for line in f.readlines()]

    numbers = []
    for line in lines:
        numbers.append(snailFishNumber(line))
        numbers[-1].reduction()

    maximum = float('-inf')
    for i in range(len(numbers)):
        for j in range(len(numbers)):
            if i == j:
                continue
                
            tempNum = snailFishNumber('[' + numbers[i].numberString() + ',' + numbers[j].numberString() + ']')
            tempNum.reduction()
            val = tempNum.magnitude()
            if val > maximum:
                maximum = val

    numbers.reverse()
    while len(numbers) != 1:
        nums = [numbers.pop(), numbers.pop()]
        numbers.append(snailFishNumber('[' + nums[0].numberString() + ',' + nums[1].numberString() + ']'))
        numbers[-1].reduction()

    part1 = numbers[0].magnitude()

    if verbose:
        print(f"\nPart 1:\nMagnitude of Result: {part1}\n\nPart 2:\nLargest Magnitude: {maximum}")

    return [part1, maximum]
    

if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds")
