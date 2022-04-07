import time

class PatternTracker:
    def __init__(self):
        self.occurances = []
        self.deltas = []
        self.patternFound = False

    def addOccurance(self, step):
        self.occurances.append(step)
        if len(self.occurances) >= 2:
            self.deltas.append(self.occurances[-1] - self.occurances[-2])

        if len(self.deltas) >= 10:
            self.patternFound = len(set(self.deltas[-10:])) == 1

def main(recipes: str ='380621'):
    # 380621 is puzzle input
    digitPatterns = {i: PatternTracker() for i in range(10)}
    scores = [3, 7]
    for i, s in enumerate(scores):
        digitPatterns[s].addOccurance(i)
        
    scoresStr = '37'
    elfIndexes = [0, 1]

    while len(scores) < int(recipes) + 10:
        scores += [int(s) for s in str(scores[elfIndexes[0]] + scores[elfIndexes[1]])]
        scoresStr += str(scores[elfIndexes[0]] + scores[elfIndexes[1]])
        for i in range(2):
            elfIndexes[i] += scores[elfIndexes[i]] + 1
            elfIndexes[i] %= len(scores)

    print(f"\nPart 1:\nNext 10 scores: {''.join(str(s) for s in scores[int(recipes):int(recipes) + 11])}")

    while recipes not in scoresStr:
        scores += [int(s) for s in str(scores[elfIndexes[0]] + scores[elfIndexes[1]])]
        scoresStr += str(scores[elfIndexes[0]] + scores[elfIndexes[1]])
        for i in range(2):
            elfIndexes[i] += scores[elfIndexes[i]] + 1
            elfIndexes[i] %= len(scores)

    print(f"\nPart 2:\nFirst occurance of {recipes}: {scoresStr.index(recipes)}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main()
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
