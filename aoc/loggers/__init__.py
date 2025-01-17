"""
Logger class for Advent of Code
"""

import argparse
import importlib
import os
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, List, Tuple

import prettytable as pt
import yaml

from ..languages import LANGS

class LoggerAction(argparse.Action):
    """
    Action to instantiate a logger class and add it to the loggers list
    """
    def __init__(self, option_strings, dest, **kwargs):
        super().__init__(option_strings, dest, **kwargs)
    
    def __call__(self, parser, namespace, values, option_string=None):
        if "loggers" not in namespace:
            namespace.loggers = []
        namespace.loggers.append(self.type(namespace))
        if len(values) and hasattr(values[0], "args"):
            namespace.loggers[-1].verbose = True
        namespace.loggers.sort()


@dataclass
class Logger(ABC):
    args: argparse.Namespace
    format: str = "DEFAULT"
    name: str = "logger"
    new_data: list[Tuple[Tuple, dict]] = field(default_factory=list)
    on_exit: List[Callable] = field(default_factory=list)
    on_log: List[Callable] = field(default_factory=list)
    verbose: bool = False

    # Default methods
    def __enter__(self) -> 'Logger':
        """
        Context manager entry point
        """
        if not self.verbose:
            self.verbose = "verbose" in self.args and self.args.verbose
        
        self.print(f"Setting up")
        self.load_data()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """
        Context manager exit point
        """
        if exc_type:
            print(exc_val)
            print(exc_tb)
            return False
        
        self.log(log_all=True, on_exit=True)
        self.print(f"Finished logging")
        print(self)
        self.save_data()
        return True

    def __str__(self) -> str:
        def lower(s: str) -> str:
            return s.lower()
        
        tables = self.get_tables(style=self.format, new_only=(self.verbose or self.format != "MARKDOWN"))
        if self.format.upper() == "MARKDOWN":
            md = f"# Advent of Code {self.name.title()}\n\nYearly {self.name} for all languages:\n\n"

            if tables:
                for title_str, _ in tables:
                    md += f"* [{title_str}](#{'-'.join(map(lower, title_str.split()))})\n\n"

                for title_str, year_table in tables:
                    md += f"\n## {title_str}\n\n"
                    md += f"[Back to top](#advent-of-code-{self.name})\n\n"
                    md += year_table.get_string() + "\n"
            else:
                md += "No data to display"

            return md
        else:
            return "\n\n".join(f"{year} {self.name.title()}:\n{table}" for year, table in tables)
        
    def __lt__(self, other: object) -> bool:
        if other_name := getattr(other, "name", ""):
            return self.name < other_name
        
        return True

    def print(self, *args, **kwargs) -> None:
        """
        Print if verbose
        """
        if self.verbose:
            print(f"{self.name.title()} Logger:", *args, **kwargs)

    def add_new_data(self, *args, **kwargs) -> None:
        """
        Add new data to the logger
        """
        self.new_data.append((args, kwargs))

    def load_data(self) -> None:
        """
        Load logger data
        """
        def log_dict(d: dict, value_key: str, keys: list[Any]=[]) -> None:
            for k, v in d.items():
                if isinstance(v, dict):
                    log_dict(v, value_key, keys + [k])
                elif k in LANGS and len(keys) == 3:
                    LANGS[k].add_part(*keys, **{value_key: v}, loggers=[self])

        if vars(self.args).get("no-load", False) or not os.path.exists(Path(Path(__file__).parent, f"{self.name}_data.yml")):
            return

        self.print("Loading data")
        
        with open(Path(Path(__file__).parent, f"{self.name}_data.yml"), "r") as f:
            data = yaml.safe_load(f)
            for d in data.values():
                if isinstance(d, dict):
                    log_dict(d, self.value_key)

        self.print("Data loaded")

    def save_data(self) -> None:
        """
        Save logger data
        """
        if vars(self.args).get("no-save", False):
            return
        
        self.print("Saving data")

        to_dump = {}
        for k, v in vars(self).items():
            if not isinstance(v, dict):
                continue

            to_dump[k] = v

        with open(Path(Path(__file__).parent, f"{self.name}_data.yml"), "w") as f:
            yaml.safe_dump(to_dump, f)

        self.print("Data saved")

    def log(self, *args, on_exit: bool=False, **kwargs) -> None:
        """
        Log a message
        """
        for new_args, new_kwargs in self.new_data:
            for k, v in kwargs.items():
                if k not in new_kwargs:
                    new_kwargs[k] = v

            for log in self.on_exit if on_exit else self.on_log:
                log(*new_args, **new_kwargs)

        self.new_data = []

    @abstractmethod
    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        """
        Add arguments to the parser. Must be a static method
        """
        pass

    @abstractmethod
    def get_tables(self, new_only: bool=False, **kwargs) -> List[Tuple[str, pt.PrettyTable]]:
        """
        Get the tables for the logger
        """
        pass


LOGGERS = []
__all__ = ["Logger", "LoggerAction", "LOGGERS"]


for filename in os.listdir(Path(__file__).parent):
    if filename.endswith(".py") and filename != "__init__.py":
        logger_name = filename[:-3]
        class_name = "".join(map(lambda s: s.title(), logger_name.split("_")))
        modname = f"aoc.loggers.{logger_name}"
        importlib.import_module(modname)
        
        if hasattr(sys.modules[modname], class_name) and issubclass(getattr(sys.modules[modname], class_name), Logger):
            LOGGERS.append((class_name, getattr(sys.modules[modname], class_name)))
            __all__.append(class_name)
            del modname

LOGGERS = {k: v for k, v in sorted(LOGGERS, key=lambda x: x[0])}
