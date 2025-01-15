import os
import platform
from pathlib import Path

from . import Language


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


