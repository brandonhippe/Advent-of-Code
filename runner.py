import sys
from language_functions import Language, get_languages

DONT_RUN = {(2019, 25)}


if __name__ == "__main__":
    if len(sys.argv) > 1 and (sys.argv[1] == "--help" or sys.argv[1] == "-h"):
        print("Usage: python(3) runner.py [year] [day] [--languages|-l] [language]")
        print("Example: python(3) runner.py 2015 1 --languages python")
        exit(0)

    ix = 1
    years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
    days = [n + 1 for n in range(25)]
    languages = []
    valid_languages = get_languages()

    while ix < len(sys.argv) and not sys.argv[ix].startswith("--") and not sys.argv[ix].startswith("-"):
        if len(years) != 1:
            years = [int(sys.argv[ix])]
        elif len(days) != 1:
            days = [int(sys.argv[ix])]
        else:
            raise ValueError(f"Unknown argument {sys.argv[ix]}")
        
        ix += 1

    if ix < len(sys.argv) and (sys.argv[ix] == "--languages" or sys.argv[ix] == "-l"):
        ix += 1
        while ix < len(sys.argv):
            if sys.argv[ix].lower() not in valid_languages:
                raise ValueError(f"Unknown language {sys.argv[ix]}")
            
            languages.append(sys.argv[ix])
            ix += 1
    else:
        languages = valid_languages
    
    if len(days) > 1:
        from Modules.progressbar import printProgressBar

    for language in languages:
        totalTime = 0
        lang = Language(language.lower())
        anyRan = False

        inLang = set()
        for year in years:
            for day in days:
                if (year, day) in DONT_RUN or not lang.exists(year, day):
                    continue

                inLang.add((year, day))
        
        if len(inLang) == 0:
            continue

        if len(languages) > 1:
            print(f"Running {language}...")

        for (i, (year, day)) in enumerate(inLang):
            if len(inLang) > 1:
                printProgressBar(i + 1, len(inLang))

            (_, p1_elapsed), (_, p2_elapsed) = lang.run(year, day, len(days) == 1)
            totalTime += p1_elapsed + p2_elapsed

        print(f"\n{language}: Total time: {totalTime:.4f} seconds\n\n")
