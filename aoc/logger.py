"""
Logger class for Advent of Code
"""

import argparse
from abc import ABC, abstractmethod
from dataclasses import dataclass 
from typing import Any, List, Tuple

import prettytable as pt


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
    name: str = "logger"
    verbose: bool = False
    format: str = "DEFAULT"

    # Default methods
    def __enter__(self) -> 'Logger':
        """
        Context manager entry point
        """
        if not self.verbose:
            self.verbose = "verbose" in self.args and self.args.verbose
        
        self.print(f"Setting up {self.name} logger")

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """
        Context manager exit point
        """
        if exc_type:
            print(exc_val)
            print(exc_tb)
            return False
        
        self.print(f"\nFinished logging {self.name}\n{self}")
        return True

    def __str__(self) -> str:
        def lower(s: str) -> str:
            return s.lower()
        
        tables = self.get_tables(style=self.format)
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
        other_name = getattr(other, "name", "")
        if not other_name:
            return True
        
        return self.name < other_name

    def print(self, *args, **kwargs) -> None:
        """
        Print if verbose
        """
        if self.verbose:
            print(*args, **kwargs)

    @abstractmethod
    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        """
        Add arguments to the parser. Must be a static method
        """
        pass

    @abstractmethod
    def log(self, msg: Any, **kwargs) -> None:
        """
        Log a message
        """
        pass

    @abstractmethod
    def get_tables(self, **kwargs) -> List[Tuple[str, pt.PrettyTable]]:
        """
        Get the tables for the logger
        """
        pass