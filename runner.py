import sys
import re
from itertools import product
from language_functions import Language, get_languages


DONT_RUN = {}


def print_help():
    print("Usage: python runner.py [--year|-y] [year(s)] [--day|-d] [day(s)] [--languages|-l] [language(s)|~language(s)] [--common|-c]")
    print("\t--year|-y: Specify year(s) to run. Default: All")
    print("\t--day|-d: Specify day(s) to run. Default: All")
    print("\t--languages|-l: Specify language(s) to run. Preface language with ~ to exclude language. Defualt: All")
    print("\t--common|-c: Run only programs that exist in all specified languages. Default: False")
    print("\t--help|-h: Show this help screen.")
    print("Example: python runner.py --year 2015 --day 1 --languages python")
    exit(0)


def contiguous_groups(l):
    l = sorted(list(set(l)))
    ranges = [(l[0], l[0])]
    for i in range(1, len(l)):
        if l[i] - l[i - 1] > 1:
            ranges[-1] = (ranges[-1][0], l[i - 1])
            ranges.append((l[i], l[i]))

    ranges[-1] = (ranges[-1][0], l[-1])
    return ranges


def run(language_year_days: dict, progressBar):
    year_days_langs = {tuple(sorted(list(year_days))): [] for year_days in language_year_days.values() if len(year_days) != 0}
    for lang, year_days in language_year_days.items():
        if len(year_days) != 0:
            year_days_langs[tuple(sorted(list(year_days)))].append(lang)
    
    for year_days, langs in year_days_langs.items():
        print(f"Running {', '.join(l.lang for l in langs)} for:")
        for year in sorted(list(set(y for y, _ in year_days))):
            days_for_year = [d for y, d in year_days if y == year]
            if len(days_for_year) == 1:
                print(f"{year}, day {days_for_year[0]}")
            else:
                ranges = contiguous_groups(days_for_year)
                print(f"{year}, days {', '.join(f'{start}-{end}' if start != end else str(start) for start, end in ranges)}")

        print()

    print("\n")

    for lang, year_days in language_year_days.items():
        totalTime = 0
        language = lang.lang

        if len(year_days) == 0:
            continue

        print(f"Running {language}...")

        for (i, (year, day)) in enumerate(year_days):
            if progressBar and i == 0:
                printProgressBar(i, len(year_days))

            (_, p1_elapsed), (_, p2_elapsed) = lang.run(year, day, not progressBar)
            totalTime += p1_elapsed + p2_elapsed

            if progressBar:
                printProgressBar(i + 1, len(year_days))

        print(f"\n{language}: Total time: {totalTime:.4f} seconds\n\n")


if __name__ == "__main__":
    if "--help" in sys.argv or "-h" in sys.argv:
        print_help()

    ix = 1
    years = []
    days = []
    languages = []
    valid_languages = set(get_languages())
    common = False
    progressBar = False
    field = None
    year_days = set()

    ix = 1
    while ix < len(sys.argv):        
        arg = sys.argv[ix]
        ix += 1

        if arg[0] == '-':
            common = common or field == 'c'
            if arg[1] == '-':
                field = arg[2]
            else:
                field = arg[1]

            continue

        if field is None:
            print("Error: invalid arguments")
            print_help()

        if field == 'y':
            nums = re.findall(r'\d+', arg)
            if len(nums) == 0:
                print("Error: invalid year")
                print_help()
            elif len(nums) == 1:
                years.append(int(nums[0]))
            else:
                for n1, n2 in zip(nums[:-1], nums[1:]):
                    if f"{n1}-{n2}" in arg:
                        years.extend(range(int(n1), int(n2) + 1))
                    else:
                        years.append(int(n1))
                        days.append(int(n2))
        elif field == 'd':
            nums = re.findall(r'\d+', arg)
            if len(nums) == 0:
                print("Error: invalid year")
                print_help()
            elif len(nums) == 1:
                days.append(int(nums[0]))
            else:
                for n1, n2 in zip(nums[:-1], nums[1:]):
                    if f"{n1}-{n2}" in arg:
                        days.extend(range(int(n1), int(n2) + 1))
                    else:
                        days.append(int(n1))
                        days.append(int(n2))
        elif field == 'l':
            if arg[0] == '~':
                valid_languages.remove(arg[1:])
            else:
                languages.append(arg)
        elif field == 'c':
            common == True

    common = common or field == 'c'

    if len(years) == 0:
        years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]

    if len(days) == 0:
        days = [n + 1 for n in range(25)]

    if len(languages) == 0:
        languages = valid_languages
    else:
        languages = list(set(languages).intersection(valid_languages))

    if len(languages) == 0:
        raise ValueError("No languages to run")

    languages = [Language(lang.lower()) for lang in sorted(languages)]
    year_days = {(year, day) for year, day in product(years, days)}
    year_days.difference_update(DONT_RUN)

    if len(year_days) == 0:
        raise ValueError("No valid years/days for the given languages")
    
    if len(year_days) > 1:
        progressBar = True
        from Modules.progressbar import printProgressBar

    if common:
        for s in [set(lang.discover()) for lang in languages]:
            year_days.intersection_update(s)

    language_year_days = {lang: year_days.intersection(set(lang.discover())) for lang in languages}
    if all(len(k) == 0 for k in language_year_days.values()):
        raise ValueError("No valid years/days for the given languages")
        
    run(language_year_days, progressBar)