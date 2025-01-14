"""
Language classes for Advent of Code.
"""

import datetime
import importlib
import os
import platform
import re
import subprocess
import sys
from abc import ABC, abstractmethod
from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, List, Optional, Tuple
from zoneinfo import ZoneInfo

import cv2
import numpy as np
import pytesseract
from advent_of_code_ocr import convert_6
from PIL import Image, ImageDraw


def get_released(year: Optional[int]=None) -> List[int]:
    """
    Get a list of released years, if no year is given.
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
class Day:
    day: int
    times: list[float] = field(default_factory=lambda: [0, 0])
    ans: list[str] = field(default_factory=lambda: ["", ""])
    combined_time: float = 0
    runtime_changed: bool = False
    ans_changed: bool = False

    def update_entity_path(self, **kwargs) -> dict:
        kwargs = deepcopy(kwargs)
        kwargs["entity_path"] = kwargs.get("entity_path", []) + [self.day]
        return kwargs

    def add_part(self, part: int, time: Optional[float]=None, ans: Optional[str]=None, loggers: List[Any]=[], **kwargs) -> None:
        if time:
            self.times[part - 1] = time
            if all(self.times) or (self.day == 25 and self.times[0]):
                self.combined_time = sum(self.times)
        if ans:
            if ans.count("\n") > 1:
                assert(set(ans) == {"█", " ", "\n"}), f"Invalid answer for {self.day} part {part}: {ans}"

                rows = [r for r in ans.split("\n") if r]
                min_ix = min(min(r.find("█") for r in rows) for r in rows)
                max_ix = max(max(r.rfind("█") for r in rows) for r in rows)
                rows = [r[min_ix:max_ix + 1] for r in rows]
                max_len = max(len(r) for r in rows)
                rows = [r.ljust(max_len) for r in rows]

                if len(rows) == 6:
                    ans = convert_6("\n".join(rows), fill_pixel="█", empty_pixel=" ")
                else:
                    # Do Optical Character Recognition
                    ### BE AMAZED IF THIS WORKS ###
                    img = Image.new("RGB", (len(rows[0]) + 2, len(rows) + 2), (255, 255, 255))
                    draw = ImageDraw.Draw(img)
                    char_in_col = set(range(len(rows[0]) + 2))
                    for y, row in enumerate(rows, 1):
                        for x, c in enumerate(row, 1):
                            if c == "█":
                                draw.point((x, y), (0, 0, 0))
                                if x in char_in_col:
                                    char_in_col.remove(x)
                            else:
                                draw.point((x, y), (255, 255, 255))
                    
                    ans = ""
                    left_side = 0
                    for right_side in sorted(char_in_col)[1::2]:
                        temp_img = img.crop((left_side, 0, right_side + 1, len(rows) + 2))
                        for _ in range(4):
                            temp_img = temp_img.resize((temp_img.width * 2, temp_img.height * 2), Image.LANCZOS)
                            temp_img = np.array(temp_img)
                            temp_img = cv2.GaussianBlur(np.array(temp_img), (3, 3), 0)
                            norm_img = np.zeros((temp_img.shape[0], temp_img.shape[1]), np.uint8)
                            temp_img = cv2.normalize(temp_img, norm_img, 0, 255, cv2.NORM_MINMAX)
                            temp_img = cv2.threshold(temp_img, 150, 255, cv2.THRESH_BINARY)[1]
                            temp_img = Image.fromarray(temp_img)

                        ans += pytesseract.image_to_string(temp_img, config="--psm 6").strip().upper()
                        left_side = right_side + 1

            self.ans[part - 1] = ans
        
        self.log(loggers, **kwargs)

    def log(self, loggers: List[Any]=[], **kwargs) -> None:
        for l in loggers:
            l.log(self, **self.update_entity_path(**kwargs))

    def __len__(self) -> int:
        return sum(bool(t) or bool(len(a)) for t, a in zip(self.times, self.ans))


@dataclass
class Year:
    avg_time: float = 0
    combined_time: float = 0
    runtimes_changed: bool = False
    ans_changed: bool = False

    def __init__(self, year: int) -> None:
        self.year = year
        self.days = {d: Day(d) for d in get_released(year)}

    def update_entity_path(self, **kwargs) -> dict:
        kwargs = deepcopy(kwargs)
        kwargs["entity_path"] = kwargs.get("entity_path", []) + [self.year]
        return kwargs

    def add_part(self, day: int, part: int, time: Optional[float]=None, ans: Optional[str]=None, loggers: List[Any]=[], **kwargs) -> None:
        self.days[day].add_part(part, time, ans, loggers, **self.update_entity_path(**kwargs))
        if self.days[day].day == 0:
            self.days[day].day = day
        
        tot_days = len(list(d for d in self.days.values() if d.combined_time))
        
        self.avg_time = (sum(d.combined_time for d in self.days.values()) / tot_days) if tot_days else 0
        if tot_days == 25:
            self.combined_time = self.avg_time * 25

        self.log(loggers, **kwargs)

    def log(self, loggers: List[Any]=[], log_sub: bool=False, **kwargs) -> None:
        if log_sub:
            for d in self.days.values():
                d.log(loggers, **self.update_entity_path(**kwargs))

        for l in loggers:
            l.log(self, **self.update_entity_path(**kwargs))

    def __len__(self) -> int:
        return sum(bool(len(d)) for d in self.days.values())


@dataclass
class Language(ABC):
    """
    Abstract class for a language used in Advent of Code.

    Methods for obtaining the parent directory, compile string, and run string are required.
    Methods for running the program and discovering all files are provided, but can be overridden.
    """
    lang: str
    folder: bool = False
    ext: str = ""
    years: dict[int, Year] = field(default_factory=lambda: {y: Year(y) for y in get_released()})
    runtimes_changed: bool = False
    ans_changed: bool = False

    def __hash__(self) -> int:
        return self.lang.__hash__()
    
    def __repr__(self) -> str:
        return self.lang
    
    def __str__(self) -> str:
        return self.lang.title()
    
    def __len__(self) -> int:
        return sum(bool(len(y)) for y in self.years.values())

    def run(self, year: int, day: int, verbose: bool=False, loggers: List[Any]=[], **kwargs) -> Tuple[Tuple[Any, float], Tuple[Any, float]]:
        """
        Run the program for the given year and day.
        Raises FileNotFoundError if the file does not exist.
        """
        if self.exists(year, day):
            results = []
            for p, (ans, time) in enumerate(self.run_func(year, day, verbose), 1):
                results.append((ans, time))
                self.add_part(year, day, p, time, ans, loggers, **kwargs)

            return tuple(results)
        
        raise FileNotFoundError(f"No file found for {year} day {day}")
    
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
    def update_entity_path(self, **kwargs) -> dict:
        kwargs = deepcopy(kwargs)
        kwargs["entity_path"] = kwargs.get("entity_path", []) + [self.lang]
        return kwargs
    
    def add_part(self, year: int, day: int, part: int, time: Optional[float]=None, ans: Optional[str]=None, loggers: list[Any]=[], **kwargs) -> None:
        if "runtimes" in kwargs:
            time = float(kwargs["runtimes"])
            del kwargs["runtimes"]
        if "answers" in kwargs:
            ans = kwargs["answers"]
            del kwargs["answers"]

        self.years[year].add_part(day, part, time=time, ans=str(ans) if ans else None, loggers=loggers, **self.update_entity_path(**kwargs))
        if self.years[year].year == 0:
            self.years[year].year = year

        self.log(loggers, **kwargs)
    
    def log(self, loggers: List[Any]=[], log_sub: bool=False, **kwargs) -> None:
        if log_sub:
            for y in self.years.values():
                y.log(loggers, log_sub, **self.update_entity_path(**kwargs))

        for l in loggers:
            l.log(self, **self.update_entity_path(**kwargs))

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


### Implementations of languages ###
class Python(Language):
    """
    Class for Python programs.
    """
    
    def __init__(self) -> None:
        super().__init__("python")
        self.ext = ".py"
    
    def run_func(self, year: int, day: int, verbose: bool=False) -> Tuple[Tuple[Any, float], Tuple[Any, float]]:
        thisDir = os.getcwd()
        pardir = self.parent_dir(year, day)

        sys.path.insert(0, str(pardir))
        code = importlib.import_module(f"{year}_{day}")
        os.chdir(pardir)

        if verbose:
            print(f"\n{self.lang.title()} {year} day {day} output:", end='')

        (p1, p1_elapsed), (p2, p2_elapsed) = code.main(verbose)

        os.chdir(thisDir)
        sys.path.pop()
        del(sys.modules[f"{year}_{day}"])
        del(code)

        return (p1, p1_elapsed), (p2, p2_elapsed)
    
    def parent_dir(self, year: int, day: int) -> Path:
        return Path(os.getcwd(), f"{year}", "python")
    
    def compile_str(self, year: int, day: int) -> str:
        return ""
    
    def run_str(self, year: int, day: int) -> str:
        return f"python {year}_{day}.py"


class Rust(Language):
    """
    Class for Rust programs.
    """
    
    def __init__(self) -> None:
        super().__init__("rust")
        self.folder = True
        self.ext = ".rs"

    def parent_dir(self, year: int, day: int) -> Path:
        return Path(os.getcwd(), f"{year}", "rust", f"rust_{year}_{day}")
    
    def compile_str(self, year: int, day: int) -> str:
        return "cargo build --release"
    
    def run_str(self, year: int, day: int) -> str:
        return "cargo run --release"
    

class C(Language):
    """
    Class for the C language.
    """

    def __init__(self) -> None:
        super().__init__("c")
        self.folder = False
        self.ext = ".c"

    def parent_dir(self, year: int, day: int) -> Path:
        return Path(os.getcwd(), f"{year}", "C")
    
    def compile_str(self, year: int, day: int) -> str:
        return f"gcc {year}_{day}.c -o {year}_{day}{'.exe' if platform.system() == 'Windows' else ''} -lm"
    
    def run_str(self, year: int, day: int) -> str:
        return f".{os.sep}{year}_{day}{'.exe' if platform.system() == 'Windows' else ''}"


def get_languages() -> dict[str, Language]:
    return {k.lower(): v() for k, v in globals().items() if isinstance(v, type) and issubclass(v, Language) and v != Language}

LANGS = {k: v for k, v in sorted(list(get_languages().items()), key=lambda x: x[0])}
