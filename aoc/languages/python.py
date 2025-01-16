import importlib
import os
import sys
from pathlib import Path
from typing import Any, Tuple

from . import Language


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
        return f"python {year}_{day}{self.ext}"