"""
Runtime logger for Advent of Code
"""

import argparse
from dataclasses import dataclass, field
from typing import Any, List, Tuple

import prettytable as pt

from .language_functions import Day, Year
from .logger import Logger, LoggerAction


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
    year_combined_data: dict[int, dict[str, float]] = field(default_factory=dict)
    year_average_data: dict[int, dict[str, float]] = field(default_factory=dict)
    name: str = "runtimes"

    @staticmethod
    def add_arguments(parser: argparse.ArgumentParser) -> None:
        """
        Add arguments to the parser
        """
        parser.add_argument("--runtimes", "-r", action=LoggerAction, nargs="*", help='Log runtimes. Add " verbose" or "v" to run in verbose mode', type=RuntimeLogger)

    def log(self, msg: Any, **kwargs) -> None:
        """
        Log a runtime
        """
        if isinstance(msg, Year):
            self.log_year(msg, **kwargs)
        elif isinstance(msg, Day):
            self.log_day(msg, **kwargs)
        
    ### Logging helper functions
    def log_year(self, year: Year, **kwargs) -> None:
        """
        Log the runtime data for a year
        """
        if not len(year):
            return
        
        assert "entity_path" in kwargs, "Entity path must be provided for runtime logging"
        lang = kwargs["entity_path"][-2]

        init_dict(self.year_combined_data, [year.year, lang])
        init_dict(self.year_average_data, [year.year, lang])
        self.year_average_data[year.year][lang] = year.avg_time
        self.year_combined_data[year.year][lang] = year.combined_time
    
    def log_day(self, day: Day, **kwargs) -> None:
        """
        Log the runtime data for a day
        """
        if not len(day):
            return
        
        assert "entity_path" in kwargs, "Entity path must be provided for runtime logging"
        lang, year = kwargs["entity_path"][-3:-1]
        
        for part, time in enumerate(day.times, 1):
            init_dict(self.part_data, [year, day.day, part, lang])
            self.part_data[year][day.day][part][lang] = time

        if day.combined_time:
            init_dict(self.day_data, [year, day.day, lang])
            self.day_data[year][day.day][lang] = day.combined_time

    def get_tables(self, **kwargs) -> List[Tuple[int, pt.PrettyTable]]:
        """
        Get runtime tables
        """
        def add_times(data: dict[Any], new_labels: dict={}, hide_no_time: bool=False) -> str:
            for ix, (lang, time) in enumerate(data.items()):
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
                longest_runtimes_table.add_row([year, day, part, lang.title(), f"{self.part_data[year][day][part][lang]:.4f}"])
            tables.append((f"Longest", longest_runtimes_table))

        for year in sorted(self.year_average_data.keys()):
            year_table = pt.PrettyTable(**kwargs)
            columns = {"Day": [], "Part": []}
            for day, day_data in sorted(self.day_data.get(year, {}).items(), key=lambda x: x[0]):
                if not len(day_data):
                    continue
                
                for part, part_data in sorted(self.part_data.get(year, {}).get(day, {}).items(), key=lambda x: x[0]):
                    if not len(part_data):
                        continue

                    add_times(part_data, {"Day": f"{day}" if part == 1 else "", "Part": f"Part {part}"})

                add_times(day_data, {"Part": "Combined"})

            add_times(self.year_average_data.get(year, {}), {"Day": "Year Average"})
            add_times(self.year_combined_data.get(year, {}), {"Day": "Year Total"}, hide_no_time=True)

            for col_label, col_data in columns.items():
                while len(col_data) < max(map(len, columns.values())):
                    col_data.append("")
                year_table.add_column(col_label.title().center(5), col_data)

            tables.append((str(year), year_table))
        
        if "style" in kwargs:
            for _, year_table in tables:
                year_table.set_style(kwargs["style"])

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
