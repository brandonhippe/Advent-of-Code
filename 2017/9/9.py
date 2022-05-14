import time
import re

class Group:
    def __init__(self, gText, gNum = 0):
        self.num = gNum + 1
        self.subGroups = []

        start = re.search('{', gText)
        while re.search('{', gText):
            start = start.span()[0] + 1
            end = start
            opened = 1
            while opened != 0:
                if gText[end] == '{':
                    opened += 1
                elif gText[end] == '}':
                    opened -= 1

                end += 1

            end -= 1             

            self.subGroups.append(Group(gText[start:end], self.num))
            gText = gText[end + 1:]
            start = re.search('{', gText)

    def score(self):
        return sum([self.num] + [s.score() for s in self.subGroups])

def main(filename):
    with open(filename, encoding='UTF-8') as f:
        text = f.readline().strip('\n')

    while re.search('!.', text):
        text = re.sub('!.', '', text, 1)

    removed = 0
    while '<' in text:
        start, end = text.index('<'), text.index('>') + 1
        text = text[:start] + text[end:]
        removed += end - start - 2

    g = Group(text[1:-1])
    print(f"\nPart 1:\nScore: {g.score()}")
    print(f"\nPart 2:\nGarbage removed: {removed}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
