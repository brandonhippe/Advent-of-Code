import time

class segment:
    def __init__(self, string):
        ends = string.split(" -> ")
        self.points = []
        self.max = 0
        for end in ends:
            temp = end.split(',')
            for (i, t) in enumerate(temp):
                temp[i] = int(t)
                if temp[i] > self.max:
                    self.max = temp[i]

            self.points.append(temp[:])

        self.horizVert = self.points[0][0] == self.points[1][0] or self.points[0][1] == self.points[1][1]
        self.lineLen = ((self.points[1][0] - self.points[0][0]) ** 2 + (self.points[1][1] - self.points[0][1]) ** 2) ** 0.5

    def markLine(self, arr):
        if self.horizVert:
            slope = [0] * 2
            for i in range(2):
                slope[i] = int((self.points[1][i] - self.points[0][i]) / self.lineLen)
            
            points = []
            point = self.points[0][:]
            points.append(point[:])
            end = self.points[1][:]
            while point != end:
                for i in range(2):
                    point[i] += slope[i]
                points.append(point[:])

            for p in points:
                arr[p[1]][p[0]] += 1
        else:
            largest = [1] * 2
            smallest = [0] * 2
            for i in range(2):
                if self.points[0][i] >= self.points[1][i]:
                    largest[i] += self.points[0][i]
                    smallest[i] += self.points[1][i]
                else:
                    largest[i] += self.points[1][i]
                    smallest[i] += self.points[0][i]

            for i in range(smallest[1], largest[1]):
                for j in range(smallest[0], largest[0]):
                    if ((i - self.points[0][1]) / (self.points[1][1] - self.points[0][1])) == ((j - self.points[0][0]) / (self.points[1][0] - self.points[0][0])):
                        arr[i][j] += 1
                    

        return arr

    
def resize(arr, newLen):
    diff = newLen - len(arr[0])
    if diff == 0:
        return arr

    template = [0] * diff
    for (i, line) in enumerate(arr):
        arr[i] = line + template

    template = [0] * newLen
    for i in range(diff):
        arr.append(template[:])

    return arr


def main():
    with open('input.txt',encoding='UTF-8') as f:
        lines = [line.strip() for line in f.readlines()]

    segments = []
    for line in lines:
        segments.append(segment(line))

    maxPoint = 0
    arr = [[0]]
    for s in segments:
        if s.horizVert:
            if s.max > maxPoint:
                maxPoint = s.max
                arr = resize(arr, maxPoint + 1)

            arr = s.markLine(arr)
    
    count = 0
    for l in arr:
        for p in l:
            if p > 1:
                count += 1

    print("Part 1: \nDangerous Points: " + str(count))

    for s in segments:
        if not s.horizVert:
            if s.max > maxPoint:
                maxPoint = s.max
                arr = resize(arr, maxPoint + 1)

            arr = s.markLine(arr)
    
    count = 0
    for l in arr:
        for p in l:
            if p > 1:
                count += 1

    print("Part 2: \nDangerous Points: " + str(count))

init_time = time.perf_counter()
main()
print(f"\nRan in {time.perf_counter() - init_time} seconds")
