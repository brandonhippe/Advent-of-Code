import sys, os, re, importlib
from collections import defaultdict
from Modules.progressbar import printProgressBar
import matplotlib.pyplot as plt


IGNORE = ['.git', '.vscode', 'Modules', 'pycache']
DONT_RUN = {(2019, 25)}


def runCode():
    runtimes = defaultdict(dict)
    results = defaultdict(dict)
    thisDir = os.getcwd()

    total = 0
    for file in os.walk(thisDir):
        if re.search('Advent-of-Code/\d+$', file[0]):
            for f in file[2]:
                if re.search('\d+_\d+.py$', f):
                    total += 1

    count = 1
    for file in os.walk(thisDir):
        if not re.search('Advent-of-Code/\d+$', file[0]):
            continue

        year = int(re.findall('\d+', file[0])[0])
        
        for f in file[2]:
            if re.search('\d+_\d+.py$', f):
                day = int(re.findall('\d+', f)[1])
                printProgressBar(count, total)
                count += 1

                if (year, day) in DONT_RUN:
                    continue

                sys.path.append(file[0])
                code = importlib.import_module(f[:-3])
                os.chdir(file[0])

                (p1, p1_elapsed), (p2, p2_elapsed) = code.main(False)
                results[year][day] = (p1, p2)
                runtimes[year][day] = (p1_elapsed, p2_elapsed)

                os.chdir(thisDir)
                sys.path.pop()
                del(sys.modules[f[:-3]])
                del(code)

    print("\n")

    sorted_runtimes = []
    for year in sorted(runtimes.keys()):
        sorted_runtimes += [[year, d] for d in runtimes[year].keys()]

    sorted_runtimes.sort(key=lambda e: sum(runtimes[e[0]][e[1]]), reverse=True)
    with open("runtimes.txt", 'w') as f:
        f.write('\n'.join(f"{year} day {day} ran in {sum(runtimes[year][day])} seconds ({runtimes[year][day][0]}, {runtimes[year][day][1]})." for year, day in sorted_runtimes))


def plotRuntimes():
    with open("runtimes.txt") as f:
        lines = [line.strip('\n') for line in f.readlines()]

    runtimes = defaultdict(dict)
    totalTimes = defaultdict(lambda: 0)
    maxRuntime = 0
    for line in lines:
        year, day, combined, p1, p2 = [float(n) for n in re.findall('\d+[.]?\d*e?-?\d*', line)]
        year = int(year)
        day = int(day)

        runtimes[year][day] = (p1, p2)
        totalTimes[year] += combined
        maxRuntime = max(maxRuntime, combined)

    fig, ax = plt.subplots(2, 2)
    for year in sorted(runtimes.keys()):
        days = [day for day in range(1, 26) if day in runtimes[year]]
        ts = [runtimes[year][day] for day in days]

        ax[0][0].plot(days, [t[0] for t in ts], label = str(year))
        ax[0][1].plot(days, [t[1] for t in ts], label = str(year))
        ax[1][0].plot(days, [sum(t) for t in ts], label = str(year))
        bar = ax[1][1].bar(year, totalTimes[year], label = str(year))
        ax[1][1].bar_label(bar, fmt='%.3f')

    for (ax_y, ax_x), t in zip([(0, 0), (0, 1), (1, 0)], ['Part 1', 'Part 2', 'Combined']):
        ax[ax_y][ax_x].set_ylim(0, 1.1 * maxRuntime)
        ax[ax_y][ax_x].set_xlim(1, 25)
        ax[ax_y][ax_x].set_xlabel('Day')
        ax[ax_y][ax_x].set_ylabel('Time (s)')
        ax[ax_y][ax_x].grid(True)
        ax[ax_y][ax_x].set_title(t)
        ax[ax_y][ax_x].legend()

    ax[1][1].set_title('Year Total Runtimes')
    ax[1][1].set_xlabel('Year')
    ax[1][1].set_ylabel('Time (s)')
    ax[1][1].set_xticks(list(totalTimes.keys()))

    plt.show()


if __name__ == "__main__":
    if input("Run Code? (y/n)\n")[0] == 'y':
        runCode()

    plotRuntimes()