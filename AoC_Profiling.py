import sys, os, re, time, importlib
from collections import defaultdict
sys.path.insert(0,"C:/Users/Brandon Hippe/Documents/Coding Projects/Advent-of-Code/Modules")
from progressbar import printProgressBar
import matplotlib.pyplot as plt


IGNORE = ['.git', '.vscode', 'Modules', 'pycache']
DONT_RUN = {(2016, 8), (2018, 10), (2019, 8), (2019, 11), (2019, 25), (2021, 13), (2022, 10)}


def main():
    with open("answers.txt", encoding="UTF-8") as f:
        lines = [line.strip('\n') for line in f.readlines()]

    answers = defaultdict(dict)
    for line in lines:
        year, day = [int(x) for x in re.findall('\d+', line.split(': ')[0])]
        answer = line.split(": ")[1].split(';')
        for i in range(len(answer)):
            try:
                answer[i] = int(answer[i])
            except ValueError:
                pass

        answers[year][day] = answer

    runtimes = defaultdict(dict)
    results = defaultdict(dict)
    thisDir = os.getcwd()

    total = 0
    for file in os.walk(thisDir):
        if any(ignore in file[0] for ignore in IGNORE) or len(re.findall('\d+', file[0])) == 0 or len(file[2]) == 0:
            continue
        
        for f in file[2]:
            if '.py' in f:
                total += 1

    count = 1
    for file in os.walk(thisDir):
        if any(ignore in file[0] for ignore in IGNORE) or len(re.findall('\d+', file[0])) == 0 or len(file[2]) == 0:
            continue

        year, day = [int(x) for x in re.findall('\d+', file[0])]
        
        for f in file[2]:
            if '.py' in f:
                printProgressBar(count, total)
                count += 1

                if (year, day) in DONT_RUN:
                    break

                sys.path.append(file[0])
                code = importlib.import_module(f[:-3])
                os.chdir(file[0])

                init_time = time.perf_counter()
                results[year][day] = code.main(False)
                runtimes[year][day] = time.perf_counter() - init_time

                os.chdir(thisDir)
                sys.path.pop()
                del(sys.modules[f[:-3]])
                del(code)

    print("\n")

    combinedTimes = []
    for k in sorted(results.keys()):
        x = []
        y = []
        for k1 in sorted(results[k].keys()):
            if results[k][k1] != answers[k][k1]:
                print(f"\nIncorrect Answer:\n{k} day {k1}:\nExpected: {answers[k][k1]}\nGot: {results[k][k1]}")

            combinedTimes.append([runtimes[k][k1], k, k1])

            x.append(k1)
            y.append(runtimes[k][k1])

        plt.plot(x, y, label = k)

    combinedTimes.sort(reverse=True, key=lambda e: e[0])
    
    with open("runtimes.txt", "w") as f:
        for i, (t, year, day) in enumerate(combinedTimes):
            s = f"{i + 1}. {year} day {day} ran in {t} seconds."
            f.write(s + '\n')
            print(s)
    
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()