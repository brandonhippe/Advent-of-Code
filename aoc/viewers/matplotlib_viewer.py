#!/usr/bin/env python3

import argparse
import math
import re
from collections import defaultdict

import matplotlib.pyplot as plt
from prettytable import PrettyTable

from Modules.progressbar import printProgressBar

from ..languages import Language, LANGS

DONT_RUN = {}


def runCode(languages_to_run: list[Language]):
    for lang in languages_to_run:
        # if len(languages_to_run) > 1:
        print(f"Running {lang.lang.title()}...")

        runtimes = defaultdict(dict)
        results = defaultdict(dict)

        all_files = lang.discover()
        total = len(all_files)
        count = 1
        for year, day in all_files:
            printProgressBar(count, total)
            count += 1

            if (year, day) in DONT_RUN:
                continue

            output = lang.run(year, day, False)
            results[year][day] = tuple(out[0] for out in output)
            runtimes[year][day] = tuple(out[1] for out in output)

        print("\n")

        sorted_runtimes = []
        for year in runtimes.keys():
            sorted_runtimes.extend((year, day) for day in runtimes[year].keys())

        sorted_runtimes.sort(key=lambda e: sum(runtimes[e[0]][e[1]]), reverse=True)
        with open(f"Runtimes/{lang.lang}_runtimes.txt", 'w') as f:
            f.write(f"Runtimes for {lang.lang.title()}:\n")
            f.write('\n'.join(f"{year} day {day} ran in {sum(runtimes[year][day])} seconds ({', '.join(str(t) for t in runtimes[year][day])})." for year, day in sorted_runtimes))


def plotRuntimes(languages_to_plot: list[str], table: bool):
    figs = []

    if table:
        language_year_table = PrettyTable()
        language_year_table.title = "Language Runtime Comparison"
        year_times = {}

    for language in languages_to_plot:
        language_text = language.title()
        with open(f"Runtimes/{language}_runtimes.txt") as f:
            lines = [line.strip('\n') for line in f.readlines()][1:]

        runtimes = defaultdict(dict)
        totalTimes = defaultdict(lambda: 0)
        maxRuntime = 0
        minRuntime = float('inf')
        for line in lines:
            info = list(map(float, re.findall(r'\d+[.]?\d*e?-?\d*', line)))
            year = int(info[0])
            day = int(info[1])
            combined = info[2]

            runtimes[year][day] = tuple(info[3:])
            totalTimes[year] += combined
            maxRuntime = max(maxRuntime, combined)
            minRuntime = min(minRuntime, combined)

        if table:
            for year in sorted(runtimes.keys()):
                runtime_table = PrettyTable()
                runtime_table.title = f"{year} Runtimes for {language_text}"
                runtime_table.field_names = ["Day", "Part 1", "Part 2", "Combined"]
                runtime_table.add_rows([tuple(map(lambda x: f"{x:.6f}" if isinstance(x, float) else x, (day, *runtimes[year][day], sum(runtimes[year][day])))) for day in sorted(runtimes[year].keys())])
                print(runtime_table)

            year_times[language_text] = totalTimes

        fig, ax = plt.subplots(2, 2)
        for year in sorted(runtimes.keys()):
            days = [day for day in range(1, 26) if day in runtimes[year]]
            ts = [runtimes[year][day] for day in days]

            ax[0][0].semilogy(days, [t[0] for t in ts], label = str(year))
            ax[0][1].semilogy(days, [t[1] for t in ts], label = str(year))
            ax[1][0].semilogy(days, [sum(t) for t in ts], label = str(year))
            bar = ax[1][1].bar(year, totalTimes[year], label = str(year))
            ax[1][1].bar_label(bar, fmt='%.3f')

        for (ax_y, ax_x), t in zip([(0, 0), (0, 1), (1, 0)], ['Part 1', 'Part 2', 'Combined']):
            ax[ax_y][ax_x].set_ylim(minRuntime / 10, 10 ** (1.1 * math.log10(maxRuntime)))
            ax[ax_y][ax_x].set_xlim(1, 25)
            ax[ax_y][ax_x].set_xlabel('Day')
            ax[ax_y][ax_x].set_ylabel('Time (s)')
            ax[ax_y][ax_x].grid(True)
            ax[ax_y][ax_x].set_title(t)
            ax[ax_y][ax_x].legend()

        fig.suptitle(f"{language_text} Runtimes")
        ax[1][1].set_title('Year Total Runtimes')
        ax[1][1].set_xlabel('Year')
        ax[1][1].set_ylabel('Time (s)')
        ax[1][1].set_xticks(list(totalTimes.keys()))

        figs.append(fig)

    if table:
        years = set()
        for language in year_times.keys():
            years.update(year_times[language].keys())

        language_year_table.add_column("Language", sorted(years))
        for language in year_times.keys():
            language_year_table.add_column(language, [f"{year_times[language][year]:.3f}" if year in year_times[language] else '' for year in sorted(years)])

        print(language_year_table)

    # Works in Linux, might not work in windows
    for fig in figs:
        plt.figure(fig.number)
        mng = plt.get_current_fig_manager()
        mng.resize(*mng.window.maxsize())

    plt.show()


if __name__ == "__main__":
    languages_iterable = list(LANGS.keys())

    parser = argparse.ArgumentParser(description="Run Advent of Code programs and plot their runtimes.")
    parser.add_argument("--run", "-r", type=str, nargs='+', choices=languages_iterable, help="Run the specified languages. Default: None")
    parser.add_argument("--plot", "-p", type=str, nargs='+', choices=languages_iterable, help="Plot the runtimes for the specified languages. Default: All, or same as --run if specified")
    parser.add_argument("--table", "-t", action='store_true', help="Print a table of the runtimes. Default: False")

    args = parser.parse_args()
    running = [LANGS[l] for l in sorted(args.run or [])]
    if args.plot:
        plotting = sorted(args.plot)
    elif args.run:
        plotting = sorted([l.lang for l in running])
    else:
        plotting = sorted(languages_iterable)

    runCode(running)
    plotRuntimes(plotting, True)
