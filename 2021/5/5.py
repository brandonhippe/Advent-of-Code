import time

def main():
    with open('input.txt',encoding='UTF-8') as f:
        lines = [line.strip() for line in f.readlines()]
    
    hvpoints = set()
    allpoints = set()
    hvcounted = set()
    allcounted = set()

    for line in lines:
        ps = line.split(" -> ")
        p1, p2 = [[int(c) for c in p.split(',')] for p in ps]

        slope = []
        for c1, c2 in zip(p1, p2):
            slope.append(0 if c1 == c2 else (1 if c2 > c1 else -1))

        p = p1
        while p != p2:
            if tuple(p) in allpoints:
                allpoints.remove(tuple(p))
                allcounted.add(tuple(p))
            elif tuple(p) not in allcounted:
                allpoints.add(tuple(p))

            if 0 in slope:
                if tuple(p) in hvpoints:
                    hvpoints.remove(tuple(p))
                    hvcounted.add(tuple(p))
                elif tuple(p) not in hvcounted:
                    hvpoints.add(tuple(p))

            for i in range(len(slope)):
                p[i] += slope[i]

        if tuple(p) in allpoints:
            allpoints.remove(tuple(p))
            allcounted.add(tuple(p))
        elif tuple(p) not in allcounted:
            allpoints.add(tuple(p))

        if 0 in slope:
            if tuple(p) in hvpoints:
                hvpoints.remove(tuple(p))
                hvcounted.add(tuple(p))
            elif tuple(p) not in hvcounted:
                hvpoints.add(tuple(p))

    print(f"\nPart 1:\nDangerous Points: {len(hvcounted)}\nPart 2:\nDangerous Points: {len(allcounted)}")

init_time = time.perf_counter()
main()
print(f"\nRan in {time.perf_counter() - init_time} seconds")
