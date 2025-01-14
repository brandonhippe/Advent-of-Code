#!/usr/bin/env python3

import argparse
from itertools import product
from typing import List, Tuple

from aoc import LANGS, Language, add_arguments, aoc, get_released
from Modules.progressbar import printProgressBar

DONT_RUN = {}


def contiguous_groups(l: List[int]) -> List[Tuple[int, int]]:
    """
    Find the contiguous groups of numbers in a list.
    """
    l = sorted(list(set(l)))
    ranges = [(l[0], l[0])]
    for i in range(1, len(l)):
        if l[i] - l[i - 1] > 1:
            ranges[-1] = (ranges[-1][0], l[i - 1])
            ranges.append((l[i], l[i]))

    ranges[-1] = (ranges[-1][0], l[-1])
    return ranges


def run(language_year_days: dict[Language, tuple[int, int]], progressBar: bool, loggers=()):
    year_days_langs: dict[tuple[tuple[int, int],], list[Language]] = {tuple(sorted(list(year_days))): [] for year_days in language_year_days.values() if len(year_days) != 0}
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
        language = lang.lang.title()

        if len(year_days) == 0:
            continue

        print(f"Running {language}...")

        for (i, (year, day)) in enumerate(year_days):
            if progressBar and i == 0:
                printProgressBar(i, len(year_days))

            for _, t in lang.run(year, day, not progressBar, loggers=loggers):
                totalTime += t

            if progressBar:
                printProgressBar(i + 1, len(year_days))

        print(f"\n{language}: Total time: {totalTime:.4f} seconds\n\n")


def main(args: argparse.Namespace):
    years = args.year
    days = args.day
    common = args.common
    languages = {l: LANGS[l] for l in sorted(args.languages) if l not in args.exclude}
    
    year_days = set((year, day) for year, day in product(years, days))
    year_days.difference_update(DONT_RUN)

    if len(year_days) == 0:
        if args.verbose:
            print("No valid years/days for the given languages")
        return

    progressBar = not args.verbose and len(year_days) > 1

    if common:
        for s in [set(lang.discover()) for lang in languages.values()]:
            year_days.intersection_update(s)

    language_year_days = {lang: sorted(list(year_days.intersection(set(lang.discover())))) for lang in languages.values()}
    if all(len(k) == 0 for k in language_year_days.values()):
        if args.verbose:
            print("No valid years/days for the given languages")
        return

    if args.verbose:
        print("Running:")

    loggers = vars(args).get("loggers", [])
    with aoc(loggers):
        run(language_year_days, progressBar, loggers)


def aoc_parser() -> argparse.ArgumentParser:
    year_iterable = get_released()
    day_iterable = list(range(1, 26))

    parser = argparse.ArgumentParser(description="Run Advent of Code solutions.")
    parser.add_argument('--year', '-y', type=int, nargs='+', default=year_iterable, help='Specify year(s) to run. Default: All')
    parser.add_argument('--day', '-d', type=int, nargs='+', default=day_iterable, help='Specify day(s) to run. Default: All')

    lang_group = parser.add_mutually_exclusive_group()
    lang_group.add_argument('--languages', '-l', type=str, nargs='+', default=LANGS.keys(), choices=LANGS.keys(), help='Specify language(s) to run. Default: All')
    lang_group.add_argument('--exclude', '-e', type=str, nargs='+', default=[], choices=LANGS.keys(), help='Exclude language(s) from running. Default: None')

    parser.add_argument('--common', '-c', action='store_true', help='Run only programs that exist in all specified languages. Default: False')
    parser.add_argument('--verbose', '-v', action='store_true', help='Print verbose output. Default: False')
   
    add_arguments(parser)
    return parser


if __name__ == "__main__":
    parser = aoc_parser()
    args = parser.parse_args()
    main(args)
