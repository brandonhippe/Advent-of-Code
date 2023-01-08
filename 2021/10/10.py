import time

class chunk:
    def __init__(self, o, parentChunk):
        self.parent = parentChunk
        self.opening = o
        self.closing = ''
        self.childs = []
        self.closed = False
        self.corrupted = False
        self.incomplete = True

    def addChar(self, c):
        added = False

        for child in self.childs:
            if not child.closed:
                added = True
                child.addChar(c)
                break

        if not added:
            if c == '(' or c == '{' or c == '[' or c == '<':
                self.childs.append(chunk(c, self))
            else:
                self.closing = c
                self.closed = True
                if not self.corrupted:
                    if self.opening == '[':
                        self.corrupted = self.closing != ']'
                    elif self.opening == '{':
                        self.corrupted = self.closing != '}'
                    elif self.opening =='(':
                        self.corrupted = self.closing != ')'
                    elif self.opening == '<':
                        self.corrupted = self.closing != '>'

        if self.corrupted and self.parent:
            self.parent.corrupted = True

    def corruptedChar(self):
        c = ''
        for child in self.childs:
            if child.corrupted:
                c += child.corruptedChar()

        if self.closed:
            c += self.closing

        return c[0]

    def autoComplete(self):
        s = ''
        for child in self.childs:
            if child.incomplete:
                s += child.autoComplete()

        if self.incomplete:
            if self.opening == '(':
                s += ')'
            elif self.opening == '{':
                s += '}'
            elif self.opening == '[':
                s += ']'
            elif self.opening == '<':
                s += '>'

        return s

    def setIncomplete(self):
        for c in self.childs:
            c.setIncomplete()
        
        self.incomplete = not self.closed
                
def score(s):
    total = 0
    for l in s:
        total *= 5
        if l == ')':
            total += 1
        elif l == ']':
            total += 2
        elif l == '}':
            total += 3
        elif l == '>':
            total += 4

    return total

def main(verbose):
    with open('input.txt', encoding='UTF-8') as f:
        lines = [line.strip() for line in f.readlines()]

    chunks = []
    for l in lines:
        chunks.append([chunk(l[0], 0)])

        for c in l[1:]:
            if chunks[-1][-1].closed:
                chunks[-1].append(chunk(c, 0))
            else :
                chunks[-1][-1].addChar(c)

        for c in chunks[-1]:
            c.setIncomplete()

    count = 0
    for group in chunks:
        for c in group:
            if c.corrupted:
                first = c.corruptedChar()

                if first == ')': 
                    count += 3
                elif first == ']': 
                    count += 57
                elif first == '}':
                    count += 1197
                elif first == '>':
                    count += 25137
                
                break

    scores = []
    for group in chunks:
        scores.append(0)
        for c in group:
            if c.incomplete and not c.corrupted:
                scores[-1] += score(c.autoComplete())

        if scores[-1] == 0:
            scores.pop()

    scores.sort()

    if verbose:
        print(f"\nPart 1:\nSyntax Error Score: {count}\n\nPart 2:\nMedian Score: {scores[int((len(scores) - 1) / 2)]}")

    return [count, scores[int((len(scores) - 1) / 2)]]

    
if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds")
