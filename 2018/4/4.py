import time
import re
from datetime import datetime
from collections import defaultdict

class event:
    def __init__(self, eventLine):
        self.time = datetime.strptime(eventLine.split(']')[0][1:], '%Y-%m-%d %H:%M')
        self.eventStr = eventLine.split(']')[1][1:]

    def __lt__(self, other):
        return self.time < other.time

def main():
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    events = []
    for line in lines:
        events.append(event(line))

    events.sort()
    
    guards = defaultdict(lambda: [defaultdict(lambda: 0), 0])
    currGuard = None
    asleepTime = 0
    for e in events:
        if 'shift' in e.eventStr:
            currGuard = int(re.findall('\d+', e.eventStr)[0])
        elif 'falls asleep' == e.eventStr:
            asleepTime = e.time.minute
        elif 'wakes up' == e.eventStr:
            for m in range(asleepTime, e.time.minute):
                guards[currGuard][0][m] += 1
                guards[currGuard][1] += 1
                
    sleepingGuard = [None, [float('-inf')]]
    for guardNum, guard in zip(guards.keys(), guards.values()):
        if guard[1] > sleepingGuard[-1][-1]:
            sleepingGuard = [guardNum, guard]

    minuteAsleep = 0
    for m, amt in zip(sleepingGuard[1][0].keys(), sleepingGuard[1][0].values()):
        if minuteAsleep not in sleepingGuard[1][0] or amt > sleepingGuard[1][0][minuteAsleep]:
            minuteAsleep = m

    print(f"\nPart 1:\nGuard ID * minute: {sleepingGuard[0] * minuteAsleep}")

    minuteAsleep = [0, 0, 0] # Guard, minute, number of times asleep
    for guardNum, guard in zip(guards.keys(), guards.values()):
        for minute, times in zip(guard[0].keys(), guard[0].values()):
            if minuteAsleep[0] not in guards or minuteAsleep[1] not in guards[minuteAsleep[0]][0] or times > minuteAsleep[2]:
                minuteAsleep = [guardNum, minute, times]

    print(f"\nPart 2:\nGuard ID * minute: {minuteAsleep[0] * minuteAsleep[1]}")

if __name__ == "__main__":
    init_time = time.perf_counter()
    main()
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
