dispPats = ['abcefg', 'cf', 'acdeg', 'acdfg', 'bcdf', 'abdfg', 'abdefg', 'acf', 'abcdefg', 'abcdfg']
occurences = {344: 'a', 204: 'b', 304: 'c', 266: 'd', 96: 'e', 396: 'f', 280: 'g'}

class code:
    def __init__(self, pattern, outputs):
        self.digitReps = [-1] * 10
        self.digitPats = [-1] * 10
        self.pattern = pattern[:]
        self.outputs = outputs[:]        
        self.pairs = {'a': '', 'b': '', 'c': '', 'd': '', 'e': '', 'f': '', 'g': ''}

        for o in range(ord('a'), ord('g') + 1):
            c = chr(o)
            freq = 0
            num = 0
            for p in pattern:
                inP = False
                for test in p:
                    if test == c:
                        inP = True
                        freq += 1
                
                if inP:
                    num += len(p)
            
            index = freq * num
            self.pairs[c] = occurences[index]
        
        self.output = 0
        for o in outputs:
            self.output *= 10
            self.output += dispPats.index(self.getStdOutput(o))

    def getStdOutput(self, output):
        new = ''
        for o in output:
            new += self.pairs[o]

        return sortStr(new)

        

    

def sortStr(s):
    ordArr = [0] * len(s)
    for (i, l) in enumerate(s):
        ordArr[i] = ord(l)
    
    ordArr.sort()
    ret = ''
    for o in ordArr:
        ret += chr(o)

    return ret

def main():
    with open('input.txt',encoding='UTF-8') as f:
        lines = [line.strip() for line in f.readlines()]

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
        count += c.output

    print("Sum of output values: " + str(count))

main()
