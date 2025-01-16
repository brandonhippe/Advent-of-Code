"""
Language classes for Advent of Code.
"""

import datetime
import importlib
import os
import re
import subprocess
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, List, Optional, Tuple
from zoneinfo import ZoneInfo


def get_released(year: Optional[int]=None) -> List[int]:
    """
    Get a list of released years, if no year is given.\\
    If a year is given, get a list of released days for the given year.
    """
    now = datetime.datetime.now(tz=ZoneInfo("America/New_York"))
    if year:
        days = []
        for d in range(1, 26):
            if datetime.datetime(year, 12, d, 0, 0, 0, tzinfo=ZoneInfo("America/New_York")) > now:
                return days
            
            days.append(d)

        return days
    
    years = []
    first_date = datetime.datetime(2015, 12, 1, 0, 0, 0, tzinfo=ZoneInfo("America/New_York"))
    while first_date < now:
        years.append(first_date.year)
        first_date = datetime.datetime(first_date.year + 1, 12, 1, 0, 0, 0, tzinfo=ZoneInfo("America/New_York"))

    return years


@dataclass
class Language(ABC):
    """
    Abstract class for a language used in Advent of Code.\\
    \\
    Methods for obtaining the parent directory, compile string, and run string are required.\\
    Methods for running the program and discovering all files are provided, but can be overridden.
    """
    lang: str
    changed: set[Tuple[int, int]] = field(default_factory=set)
    ext: str = ""
    folder: bool = False
    ran: set[Tuple[int, int]] = field(default_factory=set)

    def __hash__(self) -> int:
        return self.lang.__hash__()
    
    def __repr__(self) -> str:
        return self.lang
    
    def __str__(self) -> str:
        return self.lang.title()
    
    def __len__(self) -> int:
        return len(self.ran)

    def __lt__(self, other: 'Language') -> bool:
        return self.lang < other.lang
    
    def run_func(self, year: int, day: int, verbose: bool=False) -> Tuple[Tuple[Any, float], Tuple[Any, float]]:
        """
        Default runner function, uses the command line to run the program.
        """
        thisDir = os.getcwd()
        os.chdir(self.parent_dir(year, day))
        output = subprocess.run(self.compile_str(year, day), shell=True, capture_output=True)
        if output.returncode:
            raise ValueError(f"Failed to compile {self.lang.title()} program: {year} day {day}: {output.stderr}")
        
        output = subprocess.run(self.run_str(year, day), shell=True, capture_output=True, text=True)
        os.chdir(thisDir)

        if output.returncode:
            raise ValueError(f"Failed to run {self.lang.title()} program: {year} day {day}: {output.stderr}")
        
        if not output.stdout:
            raise ValueError(f"No output from {self.lang.title()} program: {year} day {day}")

        output = output.stdout.split("\n")
        try:
            output_start = output.index("Part 1:") - 1
        except ValueError:
            raise ValueError(f"Could not find output start for {self.lang.title()} {year} day {day}")
        output = output[output_start:]

        if verbose:
            print(f"{self.lang.title()} {year} day {day} output:", end='')
            print("\n".join(output))

        elapsed = []
        results = []
        
        in_output = False
        for line in output[output_start:]:
            if not line.startswith("Part"):
                try:
                    results[-1] = line.split(":")[1].strip()
                    in_output = True
                    continue
                except IndexError:
                    pass
            else:
                in_output = True
                results.append("")
                continue

            t = re.search(r"\d+\.\d+", line)
            if not t:
                if in_output:
                    if len(results[-1]):
                        results[-1] += "\n"
                    results[-1] += line
                continue
            
            in_output = False
            elapsed.append(float(t.group(0)))
            after_chars = line[t.end():].strip()
            if after_chars in ["ms"]:
                elapsed[-1] /= 1000
            elif after_chars in ["Âµs", "µs"]:
                elapsed[-1] /= 1000000
            elif after_chars in ["ns"]:
                elapsed[-1] /= 1000000000
            elif after_chars not in ["", "s", "seconds"]:
                raise ValueError(f"Unknown time unit {after_chars}")
            
        results.extend([None] * (len(elapsed) - len(results)))
        return tuple(zip(results, elapsed))
    
    def discover(self, p: Path=os.getcwd()) -> List[Tuple[int, int]]:
        """
        Discover all files for the given language.
        """
        if self.folder:
            filename_regex = re.compile(f"^{self.lang}_\d+_\d+$")
        else:
            filename_regex = re.compile(f"^\d+_\d+{self.ext}$")

        scripts = []
        for file in os.walk(p):
            for f in file[1 + (not self.folder)]:
                if filename_regex.match(f):
                    scripts.append(tuple(map(int, re.findall(r'\d+', f))))

        return scripts

    def exists(self, year: int, day: int) -> bool:
        """
        Check if the file exists for the given year and day.
        """
        pardir = self.parent_dir(year, day)
        if not self.folder:
            pardir = Path(pardir, f"{year}_{day}{self.ext}")
        return self.parent_dir(year, day).exists()

    def input_loc(self, year: int, day: int) -> Path:
        """
        Get the input location for the given year and day.
        """
        return Path(Path(__file__).parent, "Inputs", f"{year}_{day}.txt")

    @abstractmethod
    def parent_dir(self, year: int, day: int) -> Path:
        """
        Get the parent directory for the given year and day.
        """
        pass

    @abstractmethod
    def compile_str(self, year: int, day: int) -> str:
        """
        Get the compile string for the given year and day.
        """
        pass

    @abstractmethod
    def run_str(self, year: int, day: int) -> str:
        """
        Get the run string for the given year and day.
        """
        pass
    
    # DO NOT OVERRIDE THESE METHODS
    def run(self, year: int, day: int, verbose: bool=False, loggers: List[Any]=[], **kwargs) -> Tuple[Tuple[Any, float], Tuple[Any, float]]:
        """
        Run the program for the given year and day.
        Raises FileNotFoundError if the file does not exist.
        """
        if self.exists(year, day):
            results = []
            for part, (ans, time) in enumerate(self.run_func(year, day, verbose), 1):
                results.append((ans, time))
                self.add_part(year, day, part, ans=ans, time=time, loggers=loggers, **kwargs)

            self.changed.add((year, day))

            return tuple(results)
        
        raise FileNotFoundError(f"No file found for {year} day {day}")

    def add_part(self, year: int, day: int, *args, ans: Optional[str]=None, time: Optional[float]=None, loggers: list[Any]=[], **kwargs) -> None:
        self.ran.add((year, day))
        self.log(year, day, *args, ans=ans, time=time, lang=self.lang, loggers=loggers, **kwargs)

    def log(self, *args, loggers: List[Any]=[], **kwargs) -> None:
        for l in loggers:
            l.log(*args, **kwargs)


LANGS = []
__all__ = ["Language", "LANGS", "get_released"]


for filename in os.listdir(Path(__file__).parent):
    if filename.endswith(".py") and filename != "__init__.py":
        lang_name = filename[:-3]
        modname = f"aoc.languages.{lang_name}"
        importlib.import_module(modname)
        
        if hasattr(sys.modules[modname], lang_name.title()) and issubclass(getattr(sys.modules[modname], lang_name.title()), Language):
            LANGS.append((lang_name, getattr(sys.modules[modname], lang_name.title())))
            __all__.append(lang_name.title())
            del modname

LANGS = {k: v() for k, v in sorted(LANGS, key=lambda x: x[0])}
