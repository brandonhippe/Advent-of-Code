#!/usr/bin/env python3

import argparse
import math
import platform
import re
from collections import defaultdict
from dataclasses import dataclass, field

import matplotlib.pyplot as plt

from . import Viewer, ViewerAction


@dataclass
class FigureData:
    """
    Dataclass to store figure data
    """
    def __init__(self) -> None:
        self.fig, self.ax = plt.subplots(2, 2)
        self.lang: str = ""
        self.min_runtime: float = float('inf')
        self.max_runtime: float = 0
        self.year_data: dict[str, dict[int, float]] = defaultdict(dict)

    def format_plots(self) -> None:
        for (ax_y, ax_x), t in zip([(0, 0), (0, 1), (1, 0)], ['Part 1', 'Part 2', 'Combined']):
            self.ax[ax_y][ax_x].set_ylim(self.min_runtime / 10, 10 ** (1.1 * math.log10(self.max_runtime)))
            self.ax[ax_y][ax_x].set_xlim(1, 25)
            self.ax[ax_y][ax_x].set_xlabel('Day')
            self.ax[ax_y][ax_x].set_ylabel('Time (s)')
            self.ax[ax_y][ax_x].grid(True)
            self.ax[ax_y][ax_x].set_title(t)
            self.ax[ax_y][ax_x].legend()

        self.fig.suptitle(f"{self.lang.title()} Runtimes")
        sums = defaultdict(float)
        for l, data in sorted(self.year_data.items(), key=lambda x: x[0]):
            xs = sorted(data.keys())
            ys = list(map(lambda x: data[x] - sums[x], xs))
            bar = self.ax[1][1].bar(xs, ys, label=l, bottom=list(map(lambda x: sums[x], xs)))
            self.ax[1][1].bar_label(bar, fmt='%.3f')
            sums = defaultdict(float, {x: data[x] for x in xs})

        self.ax[1][1].set_title('Year Total Runtimes')
        self.ax[1][1].set_xlabel('Year')
        self.ax[1][1].set_ylabel('Time (s)')
        self.ax[1][1].legend()

        if platform.system() == 'Linux':
            plt.figure(self.fig.number)
            mng = plt.get_current_fig_manager()
            mng.resize(*mng.window.maxsize())
        else:
            raise NotImplementedError(f"Fullscreen not yet supported on {platform.system()}")
        
    def plot_line(self, x: list[int], y: list[float], label: str, part: int = 0, **kwargs) -> None:
        self.min_runtime = min(self.min_runtime, min(y))
        self.max_runtime = max(self.max_runtime, max(y))
        self.ax[0 if part else 1][0 if not part else part - 1].semilogy(x, y, label=label, **kwargs)

    def plot_bar(self, x: int | list[int], y: float | list[float], label: str) -> None:
        self.year_data[label].update({x: y})


@dataclass
class MatplotlibViewer(Viewer):
    """
    Matplotlib Viewer class
    """
    lang_figs: dict[str, FigureData] = field(default_factory=lambda: defaultdict(FigureData))
    name: str = "matplotlib"
    
    @staticmethod
    def add_arguments(parser: argparse.ArgumentParser) -> None:
        """
        Add arguments to the parser. Must be a static method
        """
        parser.add_argument("--matplotlib", action=ViewerAction, nargs="*", help='Run the matplotlib viewer. Add " verbose" to run in verbose mode', type=MatplotlibViewer)

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """
        Context manager exit point
        """
        if super().__exit__(exc_type, exc_val, exc_tb):
            for logger in self.loggers:
                logger.log(log_all=True, on_exit_from=type(self))
            
            for lang, fig_data in self.lang_figs.items():
                fig_data.lang = lang
                fig_data.format_plots()

            plt.show(block=True)
            
        return bool(exc_type)
    
    def __lt__(self, other: object) -> bool:
        return False
    
    ### Logging helper functions
    def log_year_avg_tot(self, time: float | list[float], year: int | list[int], lang: str, plot: str, **kwargs) -> None:
        """
        Log the average/total runtime data for a year
        """
        if not kwargs.get("log_all", False) or not isinstance(time, list) or not time:
            return
        
        assert type(time) != type(year) or len(time) == len(year), f"Data and sequence must be the same length: {time}; {year}"

        if not isinstance(year, list):
            time = [time] 
            year = [year]
        
        self.print(f"Logging {lang} {year} {plot}")
        for y, t in zip(year, time):
            self.lang_figs[lang].plot_bar(y, t, plot)
        
    def log_day(self, time: float | list[float], year: int, day: int, lang: str, **kwargs) -> None:
        """
        Log the runtime data for a day
        """
        if not kwargs.get("log_all", False) or not isinstance(time, list) or not time:
            return
        
        self.print(f"Logging {lang} {year} combined")
        self.lang_figs[lang].plot_line(day, time, str(year), color=self.entity_color([lang, year]), linewidth=2)


    def log_part(self, time: float | list[float], year: int, day: int | list[int], part: int, lang: str, **kwargs):
        """
        Log the runtime data for a part
        """
        if not kwargs.get("log_all", False) or not isinstance(time, list) or not time:
            return

        self.print(f"Logging {lang} {year} part {part}") 
        self.lang_figs[lang].plot_line(day, time, str(year), part=part, color=self.entity_color([lang, f"part{part}", year]), linewidth=2)
