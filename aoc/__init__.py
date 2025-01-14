__all__ = ["Language", "aoc", "Loggers", "RerunViewer", "LANGS", "get_released", "add_arguments"]

import argparse
import importlib
import os
from dataclasses import dataclass

from .language_functions import LANGS, Language, get_released
from .logger import Logger
from .rerun_viewer import RerunViewer

Loggers = [RerunViewer]
for path in os.listdir(os.path.dirname(__file__)):
    if path.endswith(".py") and path != "__init__.py":
        module = importlib.import_module(f"aoc.{path[:-3]}")
        for name in dir(module):
            m = getattr(module, name)
            if name != "Logger" and isinstance(m, type) and issubclass(m, Logger) and m not in Loggers:
                globals()[name] = m
                Loggers.append(m)
                del name


def add_arguments(parser: argparse.ArgumentParser) -> None:
    for m in Loggers:
        m.add_arguments(parser)


@dataclass
class aoc:
    """
    Advent of Code data class
    """
    loggers: list[Logger]

    def __enter__(self):
        for logger in self.loggers:
            logger.__enter__()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Context manager exit point
        """
        if exc_type:
            print(exc_val)
            print(exc_tb)
            return False
        
        for logger in self.loggers:
            logger.__exit__(None, None, None)

        return True
