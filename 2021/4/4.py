import time

class bingoBoard:
    def __init__(self, values):
        self.board = values[:]
        template = [0] * 5
        self.checked = []
        for _ in range (5):
            self.checked.append(template[:])

    def mark(self, call):
        for (i, row) in enumerate(self.board):
            for (j, val) in enumerate(row):
                if val == call:
                    self.checked[i][j] += 1

        for i in range(len(self.board)):
            counts = [0] * 2
            for j in range(len(self.board)):
                if self.checked[i][j] > 0:
                    counts[0] += 1
                if self.checked[j][i] > 0:
                    counts[1] += 1

            if 5 in counts:
                return 1

        return 0

    def score(self, call):
        count = 0
        for (i, row) in enumerate(self.checked):
            for (j, val) in enumerate(row):
                if val == 0:
                    count += self.board[i][j] * call

        return count

    def printBoard(self):
        for row in self.board:
            print(row)


def main(verbose):
    with open('input.txt',encoding='UTF-8') as f:
        lines = [line.strip() for line in f.readlines()]

    calls = lines.pop(0).split(',')
    lines.pop(0)

    for (i, num) in enumerate(calls):
        calls[i] = int(num)

    boards = []
    values = []
    for line in lines:
        if len(line) == 0:
            boards.append(bingoBoard(values))
            values = []
        else:
            temp = line.split(' ')
            for i in range(len(temp) - 1, -1, -1):
                if len(temp[i]) == 0:
                    temp.pop(i)
                else:
                    temp[i] = int(temp[i])

            values.append(temp)

    finished = False
    for num in calls:
        for board in boards:
            won = board.mark(num)
            if won == 1:
                part1 = board.score(num)
                finished = True
                break

        if finished:
            break

    for num in calls:
        for i in range(len(boards) - 1, -1, -1):
            won = boards[i].mark(num)
            if won == 1:
                if len(boards) == 1:
                    part2 = boards[i].score(num)
                
                boards.pop(i)
        
        if len(boards) == 0:
            break

    if verbose:
        print(f"\nPart 1:\nWinning board score: {part1}\n\nPart 2:\nLast board score: {part2}")

    return [part1, part2]


if __name__ == "__main__":
    init_time = time.perf_counter()
    main(True)
    print(f"\nRan in {time.perf_counter() - init_time} seconds")
