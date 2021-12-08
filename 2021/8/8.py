numSegs = [6, 2, 5, 5, 4, 5, 6, 3, 7, 6]
dispPats = ['abcefg', 'cf', 'acdeg', 'acdfg', 'bcdf', 'abdfg', 'abdefg', 'acf', 'abcdefg', 'abcdfg']

class code:
    def __init__(self, pattern, outputs):
        self.digitReps = [-1] * 10
        self.digitPats = [-1] * 10
        self.posLetters = ['abcdefg'] * 7
        self.pattern = [''] * 10
        self.outputs = [''] * 4

        for (j, p) in enumerate(pattern):
            patternAscii = [0] * len(p)
            for (i, l) in enumerate(p):
                patternAscii[i] = ord(l)

            patternAscii.sort()
            for n in patternAscii:
                self.pattern[j] += chr(n)

        for (j, o) in enumerate(outputs):
            outputsAscii = [0] * len(o)
            for (i, l) in enumerate(o):
                outputsAscii[i] = ord(l)

            outputsAscii.sort()
            for n in outputsAscii:
                self.outputs[j] += chr(n)
            


        for p in self.pattern:
            if len(p) == 2 or len(p) == 3 or len(p) == 4 or len(p) == 7:
                i = 0
                index = self.hash(p, i)
                while self.digitReps[index] != -1:
                    i += 1
                    index = self.hash(p, i)

                num = numSegs.index(len(p))
                self.digitPats[index] = p
                self.digitReps[index] = num
                for l in dispPats[num]:
                    self.updatePossible(l, p[:])

    def hash(self, digit, collison):
        count = collison
        for c in digit:
            count += ord(c)

        return count % 10

    def letterIndex(self, letter):
        return ord(letter) - ord('a')

    def updatePossible(self, letter, pat):
        index = self.letterIndex(letter)
        for l in self.posLetters[index]:
            if l not in pat:
                self.posLetters[index] = self.removeChar(self.posLetters[index], l)

    def removeChar(self, letters, l):
        try:
            i = letters.index(l)
        except ValueError:
            return letters
        temp = letters[:i]
        temp = temp + letters[i + 1:]
        return temp


    def genOutput(self):
        while True:
            # Update Possible Letters (Finds the top segment and 3 pairs)
            prev = self.posLetters[:]

            for pos in self.posLetters:
                if self.posLetters.count(pos) == len(pos):
                    for (i, remove) in enumerate(self.posLetters):
                        if remove != pos:
                            for l in pos:
                                self.posLetters[i] = self.removeChar(self.posLetters[i], l)

            if prev == self.posLetters:
                break

        # Work cases by length (3 length 5, 3 length 6)
        for p in self.pattern:
            if not (len(p) == 5 or len(p) == 6):
                continue

            i = 0
            index = self.hash(p, i)
            while self.digitReps[index] != -1:
                i += 1
                index = self.hash(p, i)

            if len(p) == 5:
                # 2 is only case to use 'eg' pair, 5 is only case to use 'bd', 3 only uses one of each
                eg = self.posLetters[self.letterIndex('e')][:]
                bd = self.posLetters[self.letterIndex('b')][:]
                egIn = True
                bdIn = True

                for i in range(2):
                    if eg[i] not in p:
                        egIn = False
                    if bd[i] not in p:
                        bdIn = False

                if egIn:
                    num = 2
                elif bdIn:
                    num = 5
                else:
                    num = 3
            elif len(p) == 6:
                # 0 is missing 'bd' pair, 6 is missing 'cf' pair, 9 is missing 'eg' pair
                eg = self.posLetters[self.letterIndex('e')][:]
                cf = self.posLetters[self.letterIndex('c')][:]
                bd = self.posLetters[self.letterIndex('b')][:]
                egIn = True
                cfIn = True
                bdIn = True

                for i in range(2):
                    if eg[i] not in p:
                        egIn = False
                    if cf[i] not in p:
                        cfIn = False
                    if bd[i] not in p:
                        bdIn = False

                if not bdIn:
                    num = 0
                elif not cfIn:
                    num = 6
                else:
                    num = 9

            self.digitPats[index] = p
            self.digitReps[index] = num

        count = 0
        for o in self.outputs:
            i = 0
            index = self.hash(o, i)
            while not self.digitPats[index] == o:
                i += 1
                index = self.hash(o, i)

            count *= 10
            count += self.digitReps[index]

        return count

def main():
    with open('input.txt',encoding='UTF-8') as f:
        lines = f.readlines()

    patterns = []
    outputs = []

    for line in lines:
        temp = line.split(" | ")
        patterns.append(temp[0])
        outputs.append(temp[1])

    for (i, pattern) in enumerate(patterns):
        patterns[i] = pattern.split(' ')

    for (i, output) in enumerate(outputs):
        outputs[i] = output.split(' ')

    for output in outputs:
        for (i, o) in enumerate(output):
            if o[-1] == '\n':
                output[i] = o[0:-1]

    print("Part 1:")
    count = 0
    for output in outputs:
        for o in output:            
            if len(o) == 2 or len(o) == 3 or len(o) == 4 or len(o) == 7:
                count += 1

    print("Instances of 1, 4, 7, and 8: " + str(count))

    print("Part 2:")
    count = 0
    for i in range(len(patterns)):
        c = code(patterns[i], outputs[i])
        count += c.genOutput()

    print("Sum of output values: " + str(count))

main()
