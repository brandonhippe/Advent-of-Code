import sys, os, importlib


DONT_RUN = {(2019, 25)}


if __name__ == "__main__":
    if len(sys.argv) == 3:
        year, day = [int(n) for n in sys.argv[1:]]
        days = [day]
    elif len(sys.argv) == 2:
        year = int(sys.argv[1])
        days = [n + 1 for n in range(25)]
    else:
        raise ValueError("Invalid number of arguments passed")
    
    if len(days) > 1:
        from Modules.progressbar import printProgressBar

    totalTime = 0
    currDir = os.getcwd()
    for i, day in enumerate(days):
        if len(days) > 1:
            printProgressBar(i + 1, len(days))

            if (year, day) in DONT_RUN:
                continue

        sys.path.append(os.path.join(os.getcwd(), str(year)))
        code = importlib.import_module(f'{year}_{day}')

        os.chdir(os.path.join(os.getcwd(), str(year)))
        (_, p1_elapsed), (_, p2_elapsed) = code.main(len(days) == 1)
        os.chdir(currDir)

        totalTime += p1_elapsed + p2_elapsed

    print(f"\nTotal time: {totalTime:.4f} seconds")