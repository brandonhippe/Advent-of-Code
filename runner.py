import sys, os, importlib


if __name__ == "__main__":
    year, day = [int(n) for n in sys.argv[1:]]

    sys.path.append(os.path.join(os.getcwd(), str(year)))
    code = importlib.import_module(f'{year}_{day}')
    os.chdir(os.path.join(os.getcwd(), str(year)))
    code.main(True)