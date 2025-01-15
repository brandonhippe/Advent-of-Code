"""
Viewer class for Advent of Code
"""

import argparse
import importlib
import os
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

import yaml


class ViewerAction(argparse.Action):
    """
    Action to instantiate a viewer class and add it to the viewers list
    """
    def __init__(self, option_strings, dest, **kwargs):
        super().__init__(option_strings, dest, **kwargs)
    
    def __call__(self, parser, namespace, values, option_string=None):
        if "viewers" not in namespace:
            namespace.viewers = []
        namespace.viewers.append(self.type(namespace))
        if len(values) and hasattr(values[0], "args"):
            namespace.viewers[-1].verbose = True
        namespace.viewers.sort()


@dataclass
class Viewer(ABC):
    """
    Abstract class for a viewer
    """
    args: argparse.Namespace
    name: str = "viewer"
    verbose: bool = False

    # Default methods
    def __enter__(self) -> 'Viewer':
        """
        Context manager entry point
        """
        if not self.verbose:
            self.verbose = vars(self.args).get("verbose", False)
        
        self.loggers = vars(self.args).get("loggers", [])
        self.attach_to_loggers()
        self.print(f"Setting up {self.name} viewer")

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """
        Context manager exit point
        """
        if exc_type:
            print(exc_val)
            print(exc_tb)
            return False
        
        self.print(f"\nFinished {self.name} viewer")
        return True
        
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

    def load_data(self) -> None:
        """
        Load saved data for the viewer
        """
        pass

    def save_data(self) -> None:
        """
        Save the viewer data
        """
        pass

    def attach_to_loggers(self) -> None:
        """
        Attach the viewer to the loggers
        """
        with open(Path(Path(__file__).parent, f"{self.name}.yml"), "r") as f:
            viewer_config = yaml.safe_load(f)

        for logger in self.args.loggers:
            for arr_name, to_attach in viewer_config.items():
                to_attach = to_attach[0]
                if logger.name in to_attach:
                    callables = getattr(logger, arr_name)
                    callables.append(getattr(self, to_attach[logger.name]))
                    setattr(logger, arr_name, callables)

    @abstractmethod
    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        """
        Add arguments to the parser. Must be a static method
        """
        pass


VIEWERS = []
__all__ = ["Viewer", "ViewerAction", "VIEWERS"]


for filename in os.listdir(Path(__file__).parent):
    if filename.endswith(".py") and filename != "__init__.py":
        viewer_name = filename[:-3]
        class_name = "".join(map(lambda s: s.title(), viewer_name.split("_")))
        modname = f"aoc.viewers.{viewer_name}"
        importlib.import_module(modname)
        
        if hasattr(sys.modules[modname], class_name) and issubclass(getattr(sys.modules[modname], class_name), Viewer):
            VIEWERS.append((class_name, getattr(sys.modules[modname], class_name)))
            __all__.append(class_name)
            del modname

VIEWERS = {k: v for k, v in sorted(VIEWERS, key=lambda x: x[0])}
