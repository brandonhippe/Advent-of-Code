"""
Viewer class for Advent of Code
"""

import argparse
import importlib
import os
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import yaml
from matplotlib import colormaps, colors

from ..languages import LANGS, get_released
from ..loggers import Logger

COLOR_MAP = colormaps['tab10']


def map_to_entity_path(entity_path: list[Any]) -> str:
    """
    Convert a list of entities to an entity path
    """
    if not entity_path or not entity_path[0].startswith("+"):
        entity_path = [""] + entity_path
    return "/".join(map(str, entity_path))


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
    colormap: dict = field(default_factory=dict)
    loggers: list[Logger] = field(default_factory=list)
    name: str = "viewer"
    verbose: bool = False

    # Default methods
    def __enter__(self) -> 'Viewer':
        """
        Context manager entry point
        """
        if not self.verbose:
            self.verbose = vars(self.args).get("verbose", False)
        
        self.print(f"Setting up")
        self.loggers = vars(self.args).get("loggers", [])
        self.attach_to_loggers()

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """
        Context manager exit point
        """
        if exc_type:
            print(exc_val)
            print(exc_tb)
            return False
        
        self.print(f"Finished")
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
            print(f"{self.name.title()} Viewer:", *args, **kwargs)

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
        fpath = Path(Path(__file__).parent, f"{self.name}.yml")

        if os.path.exists(fpath):
            with open(fpath, "r") as f:
                viewer_config = yaml.safe_load(f)
        else:
            viewer_config = {"post_log": [{"runtimes": "log"}]}

        for logger in self.loggers:
            for arr_name, to_attach in viewer_config.items():
                to_attach = to_attach[0]
                if logger.name in to_attach:
                    callables = getattr(logger, arr_name)
                    callables.append(getattr(self, to_attach[logger.name]))
                    setattr(logger, arr_name, callables)

    def log(self, *args, ans: Optional[Any]=None, time: Optional[float]=None, on_exit_from: Optional[type]=None, **kwargs):
        """
        Default logging function\\
        Used by both rerun and matplotlib viewers\\
        Attaches to runtime logger as a post-log action\\
        """
        if on_exit_from is not None and type(self) != on_exit_from:
            return
        
        entity_path = args
        if time:
            if len(entity_path) == 4:
                self.log_part(time, *args, **{k: v for k, v in kwargs.items() if k != "lang"})
            elif len(entity_path) == 3:
                if entity_path[-1] == kwargs["lang"]:
                    self.log_day(time, *args, **{k: v for k, v in kwargs.items() if k != "lang"})
                else:
                    self.log_year_avg_tot(time, *args, **{k: v for k, v in kwargs.items() if k != "lang"})
            else:
                raise ValueError(f"Unknown entity path: {map_to_entity_path(entity_path)}")
            
    ### Helper functions for logging
    def entity_color(self, entity_path: list[str]) -> Optional[tuple[float, float, float, float]]:
        """
        Set the color of the entity based on the last part of the path that has a color
        """
        ### Assemble the current entity colors
        entity_path = list(map(str, entity_path))
        for i, l in enumerate(sorted(LANGS.keys())):
            self.colormap[l] = COLOR_MAP(i % COLOR_MAP.N)

        for i, y in enumerate(sorted(get_released())):
            self.colormap[str(y)] = COLOR_MAP(i % COLOR_MAP.N)

        # Get the color of the last part of the entity path that has a color
        for p in entity_path[::-1]:
            if p in self.colormap:
                if 'avg' in entity_path:
                    return colors.to_rgba(self.colormap[p], alpha=0.5)
                return colors.to_rgba(self.colormap[p])

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
