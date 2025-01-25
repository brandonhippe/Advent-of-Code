__all__ = [
    "aoc",
    "LANGS",
    "Language",
    "LOGGERS",
    "Logger",
    "VIEWERS",
    "Viewer",
    "get_released",
    "add_arguments",
]

import argparse
from dataclasses import dataclass, field
from typing import List

from .languages import LANGS, Language, get_released
from .loggers import LOGGERS, Logger
from .viewers import VIEWERS, Viewer


def add_arguments(parser: argparse.ArgumentParser) -> None:
    for mod in list(LOGGERS) + list(VIEWERS):
        mod.add_arguments(parser)


@dataclass
class aoc:
    """
    Advent of Code data class
    """

    args: argparse.Namespace
    loggers: List[Logger] = field(init=False)
    viewers: List[Viewer] = field(init=False)

    def __post_init__(self) -> None:
        self.loggers = LOGGERS(self.args)
        self.viewers = VIEWERS(self.args)

    def __enter__(self):
        for mod in self.loggers + self.viewers:
            mod.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Context manager exit point
        """
        if exc_type:
            print(exc_val)
            print(exc_tb)
            return False

        for mod in self.loggers + self.viewers:
            mod.__exit__(None, None, None)

        return True
