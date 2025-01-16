"""
Runtime logger for Advent of Code
"""

import argparse
from collections import defaultdict
from dataclasses import dataclass, field
from functools import reduce
from typing import Any, List, Optional, Tuple

import prettytable as pt

from ..languages import LANGS
from . import Logger, LoggerAction


def init_dict(dict: dict[Any], keys: List[Any]):
    """
    Initialize a multi-level dictionary
    """
    key = keys[0]
    if len(keys) == 1:
        if key not in dict:
            dict[key] = 0.0
    else:
        if key not in dict:
            dict[key] = {}
        init_dict(dict[key], keys[1:])


@dataclass
class RuntimeLogger(Logger):
    """
    Runtime logger for Advent of Code
    """
    part_data: dict[int, dict[int, dict[int, dict[str, float]]]] = field(default_factory=dict)
    day_data: dict[int, dict[int, dict[str, float]]] = field(default_factory=dict)
    year_average_data: dict[int, dict[str, float]] = field(default_factory=dict)
    year_total_data: dict[int, dict[str, float]] = field(default_factory=dict)
    name: str = "runtimes"
    value_key: str = "time"

    @staticmethod
    def add_arguments(parser: argparse.ArgumentParser) -> None:
        """
        Add arguments to the parser
        """
        parser.add_argument("--runtimes", "-r", action=LoggerAction, nargs="*", help='Log runtimes. Add " verbose" or "v" to run in verbose mode', type=RuntimeLogger)
        parser.add_argument("--no-load", action="store_true", help="Don't load existing advent of code data")
        parser.add_argument("--no-save", action="store_true", help="Don't save advent of code data")

    def log(self, *args, **kwargs) -> None:
        """
        Log a runtime
        """        
        if not kwargs.get("log_all", False):
            self.log_part(*args, **kwargs)
        else: 
            for part in range(3):
                for year, y in sorted(self.part_data.items() if part else self.day_data.items(), key=lambda x: x[0]):
                    data = defaultdict(lambda: ([], []))
                    for day, day_data in sorted(y.items(), key=lambda x: x[0]):
                        if part:
                            day_data = day_data[part]
                        for lang, time in day_data.items():
                            data[lang][0].append(day)
                            data[lang][1].append(time)
                    
                    for lang, (days, times) in sorted(data.items(), key=lambda x: x[0]):
                        if part:
                            self.add_new_data(year, days, part, lang, time=times, lang=lang)
                        else:
                            self.add_new_data(year, days, lang, time=times, lang=lang)

            for d, name in zip((self.year_average_data, self.year_total_data), ("avg", "tot")):
                data = defaultdict(lambda: ([], []))
                for year in sorted(d.keys()):
                    for lang, time in sorted(d[year].items(), key=lambda x: x[0]):
                        data[lang][0].append(year)
                        data[lang][1].append(time)

                for lang, (years, times) in sorted(data.items(), key=lambda x: x[0]):
                    self.add_new_data(years, lang, name, time=times, lang=lang)

        super().log(*args, **kwargs)
        
    ### Logging helper functions
    def log_part(self, year: int, day: int, part: int, lang: Optional[str]=None, time: Optional[float]=None, **kwargs) -> None:
        """
        Log the runtime data for a part
        """
        if time is None:
            return
        
        if not all((lang, year, day, part)):
            raise ValueError("Language, year, day, and part must be provided for runtime logging")
        
        if part:
            init_dict(self.part_data, [year, day, part, lang])
            self.part_data[year][day][part][lang] = time
            self.add_new_data(year, day, part, lang, time=time)
        
        finished_parts = [p for p in self.part_data[year][day].keys() if lang in self.part_data[year][day][p]]
        if len(finished_parts) != 2:
            return

        init_dict(self.day_data, [year, day, lang])
        self.day_data[year][day][lang] = sum(self.part_data[year][day][p][lang] for p in finished_parts)
        self.add_new_data(year, day, lang, time=self.day_data[year][day][lang])

        finished_days = [d for d in self.day_data[year].keys() if lang in self.day_data[year][d]]
        init_dict(self.year_average_data, [year, lang])
        self.year_average_data[year][lang] = sum(self.day_data[year][d][lang] for d in finished_days) / len(finished_days)
        self.add_new_data(year, lang, "avg", time=self.year_average_data[year][lang])

        if len(finished_days) == 25:
            init_dict(self.year_total_data, [year, lang])
            self.year_total_data[year][lang] = sum(self.day_data[year][d][lang] for d in finished_days)
            self.add_new_data(year, lang, "tot", time=self.year_total_data[year][lang])

    def get_tables(self, new_only: bool=False, **kwargs) -> List[Tuple[int, pt.PrettyTable]]:
        """
        Get runtime tables
        """
        def add_times(data: dict[Any], new_labels: dict={}, hide_no_time: bool=False) -> str:
            for ix, (lang, time) in enumerate(sorted(data.items(), key=lambda x: x[0])):
                if lang not in columns:
                    columns[lang] = []

                while len(columns[lang]) < max(map(len, columns.values())):
                    columns[lang].append("")
                
                if ix == 0:
                    columns[lang].append("")
                if not hide_no_time or time:
                    columns[lang][-1] = f"{time:.4f}"

            for col, label in new_labels.items():
                while len(columns[col]) < max(map(len, columns.values())):
                    columns[col].append("")

                columns[col][-1] = label

        tables = []
        for k, v in kwargs.items():
            if hasattr(pt, v):
                kwargs[k] = getattr(pt, v)

        if longest_runtimes := self.longest_runtimes():
            longest_runtimes_table = pt.PrettyTable(**kwargs)
            longest_runtimes_table.field_names = ["Year", "Day", "Part", "Language", "Time"]
            for year, day, part, lang in longest_runtimes:
                if not new_only or (year, day) in LANGS[lang].changed:
                    longest_runtimes_table.add_row([year, day, part, lang.title(), f"{self.part_data[year][day][part][lang]:.4f}"])
            if len(longest_runtimes_table._rows):
                tables.append((f"Longest", longest_runtimes_table))

        changed = reduce(lambda x, y: x.union(y), [lang.changed for lang in LANGS.values()], set())
        for year in sorted(self.year_average_data.keys()):
            year_table = pt.PrettyTable(**kwargs)
            columns = {"Day": [], "Part": []}
            for day, day_data in sorted(self.day_data.get(year, {}).items(), key=lambda x: x[0]):
                if not len(day_data) or (new_only and (year, day) not in changed):
                    continue
                
                for part, part_data in sorted(self.part_data.get(year, {}).get(day, {}).items(), key=lambda x: x[0]):
                    if not len(part_data):
                        continue

                    add_times(part_data, {"Day": f"{day}" if part == 1 else "", "Part": f"Part {part}"})

                add_times(day_data, {"Part": "Combined"})

            if len(columns["Day"]) == 0:
                continue

            add_times(self.year_average_data.get(year, {}), {"Day": "Year Average"})
            add_times(self.year_total_data.get(year, {}), {"Day": "Year Total"}, hide_no_time=True)

            for col_label, col_data in columns.items():
                while len(col_data) < max(map(len, columns.values())):
                    col_data.append("")
                year_table.add_column(col_label.title().center(5), col_data)

            tables.append((str(year), year_table))
        
        if s := kwargs.get("style", False):
            for _, year_table in tables:
                year_table.set_style(s)

        return tables

    def longest_runtimes(self, n_longest: int=10) -> List[Tuple[Any,]]:
        def collect_runtimes(runtime_data: dict[Any], indecies: Tuple[Any,]=()) -> None:
            for k, v in runtime_data.items():
                if isinstance(v, dict):
                    collect_runtimes(v, indecies + (k,))
                else:
                    all_parts[indecies + (k,)] = v
        
        all_parts = {}
        collect_runtimes(self.part_data)
        sorted_ixs = sorted(all_parts, key=lambda x: all_parts[x], reverse=True)
        return sorted_ixs[:n_longest]
