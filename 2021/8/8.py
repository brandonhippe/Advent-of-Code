import time

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

def main(verbose):
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

    count = 0
    for output in outputs:
        for o in output:            
            if len(o) == 2 or len(o) == 3 or len(o) == 4 or len(o) == 7:
                count += 1

    part1 = count

    count = 0
    for i in range(len(patterns)):
        c = code(patterns[i], outputs[i])
        count += c.output

    if verbose:
        print(f"\nPart 1:\nInstances of 1, 4, 7, and 8: {part1}\n\nPart 2:\nSum of output values: {count}")

    return [part1, count]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds")
