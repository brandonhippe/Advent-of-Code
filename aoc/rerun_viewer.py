"""
Rerun viewer for profiled AOC code
"""

import argparse
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional
from uuid import uuid4

import rerun as rr
from matplotlib import colormaps, colors

from .language_functions import LANGS, Day, Language, Year
from .logger import LoggerAction, Logger
from .Blueprints import *

COLOR_MAP = colormaps['tab10']


def map_to_entity_path(entity_path: list[Any]) -> str:
    """
    Convert a list of entities to an entity path
    """
    if not entity_path or not entity_path[0].startswith("+"):
        entity_path = [""] + entity_path
    return "/".join(map(str, entity_path))


@dataclass
class RecordingWithInitialized:
    """
    Recording stream with initialized entities
    """

    def __init__(self, application_id: str, recording: Optional[rr.RecordingStream] = None, **kwargs):
        self.uuid = uuid4()
        self.initialized_entities = set()
        if recording is None:
            recording = rr.new_recording(application_id=application_id, recording_id=self.uuid, **kwargs)
        self.recording = recording

    def initialize(self, entity_path: str | list[Any]) -> bool:
        """
        Initialize an entity path for logging, if not already initialized
        """
        if not self.recording:
            self.recording = rr.get_global_data_recording()

        if isinstance(entity_path, list):
            entity_path = map_to_entity_path(entity_path)

        if entity_path not in self.initialized_entities:
            self.initialized_entities.add(entity_path)
            return True
        return False


@dataclass
class RerunViewer():
    """
    Class to handle runtime data for Advent of Code solutions\\
    Displays the data in a rerun viewer
    """
    args: argparse.Namespace
    application_id: str = "Advent of Code"
    blueprint_dir: Path = Path(Path(__file__).parent, "Blueprints")
    log_file: Path = Path(blueprint_dir, f"{''.join(map(lambda s: s[0].lower(), application_id.split(' ')))}.rrd")
    colormap: dict = field(default_factory=dict)
    blueprint_yamls: dict[str, dict] = field(default_factory=dict)
    initialized_entities: set[str] = field(default_factory=set)
    loggers: list[Logger] = field(default_factory=list)
    verbose: bool = False

    @staticmethod
    def add_arguments(parser: argparse.ArgumentParser):
        """
        Add arguments to the parser
        """
        parser.add_argument("--rerun", action=LoggerAction, nargs="*", help='Run the rerun viewer. Add " verbose" to run in verbose mode', type=RerunViewer)
        
        parser.add_argument("--default-blueprint", type=str, default=Path(Path(__file__).parent, "Blueprints", "main.yml"), help="Path to yaml that defines the base level blueprint")
        parser.add_argument("--no-blueprint", action="store_true", help="Don't load any blueprints")

        parser.add_argument("--no-load", action="store_true", help="Don't load existing advent of code data from an RRD file")
        parser.add_argument("--no-save", action="store_true", help="Don't save advent of code data to an RRD file")
        rr.script_add_args(parser)

    def start_viewer(self, load_rrd: bool=True):
        """
        Start the rerun viewer
        """

        self.active_recording = RecordingWithInitialized(application_id=self.application_id, make_default=True, make_thread_default=True)
        rr.init(application_id=self.application_id, spawn=True, recording_id=self.active_recording.uuid)

        if load_rrd:
            self.load_rrd()
        self.log_everything()

    ### Context manager functions
    def __enter__(self) -> 'RerunViewer':
        """
        Setup the rerun viewer
        """
        if not self.verbose:
            self.verbose = "verbose" in self.args and self.args.verbose

        self.loggers = vars(self.args).get("loggers", [])

        self.print("Setting up rerun viewer")
        self.start_viewer()
        
        self.p_verbose = self.args.verbose
        self.verbose = False

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """
        Exit, spawning the rerun viewer if no errors occurred
        """
        if exc_type:
            print(exc_val)
            print(exc_tb)
        else:
            self.verbose = self.p_verbose
            
            self.save()
            self.start_viewer(load_rrd=False)
            self.print("Finished logging to rerun viewer")

        rr.script_teardown(self.args)
        return bool(exc_type)
    
    def __lt__(self, other: object) -> bool:
        return False

    def print(self, *args, **kwargs):
        """
        Print if verbose
        """
        if self.verbose:
            print(*args, **kwargs)

    ### Loading/saving functions
    def save(self):
        """
        Save the current runtime data to an RRD file
        """
        if vars(self.args).get("no_save", False):
            return
        
        self.active_recording = RecordingWithInitialized(application_id=self.application_id, make_default=False, make_thread_default=False)
        default_blueprint = None if vars(self.args).get("no-blueprint", False) else load_blueprint(self.args.default_blueprint, blueprint_dir=self.blueprint_dir, loggers=self.loggers[:-1])
        rr.save(self.log_file, default_blueprint=default_blueprint, recording=self.active_recording.recording)
        self.log_everything()

    def load_rrd(self) -> bool:
        """
        Load an existing rrd file
        """
        def load_from_table(entity_name: str, data_col_start: int):
            entity_path = map_to_entity_path([entity_name])

            text_view = recording.view(index="log_tick", contents={entity_path: ["Text"]})
            if len(text_view.schema().component_columns()):
                text_view = text_view.filter_is_not_null(text_view.schema().component_columns()[0])
                text_table = text_view.select(text_view.schema().component_columns()[0]).read_pandas()
                table = text_table.iloc[-1].iloc[0][0].split("\n")

                year = None
                day = None
                lang_order = None
                lang_data = set()
                for line in table[2:]:
                    year_match = re.search(r"## (\d+)", line)
                    if year_match:
                        if lang_order:
                            self.print(f"{year}: Discovered {entity_name} in languages: {', '.join(l.title() for l in sorted(lang_data))}")

                        day = None
                        lang_order = None
                        lang_data.clear()
                        year = int(year_match.group(1))
                        
                    if not year:
                        continue

                    table_init_match = re.search(r"Day", line)
                    if table_init_match:
                        lang_order = [l.strip().lower() for l in line.split("|")[data_col_start:-1]]

                    if not lang_order:
                        continue

                    day_match = re.search(r"^\|\s*(\d+)", line)
                    if day_match:
                        day = int(day_match.group(1))
                    
                    if line and day:
                        m = re.search(r"Part (\d+)", line)
                        if not m and data_col_start != 2:
                            continue
                        
                        if m:
                            part = int(m.group(1))
                        else:
                            part = 2 - (day_match is not None)
                        for lang, data in zip(lang_order, line.split("|")[data_col_start:-1]):
                            if data := data.strip():
                                if lang not in LANGS:
                                    raise ValueError(f"Language {lang.title()} not found in available languages")
                                lang_data.add(lang)
                                kwargs = {entity_name: data}
                                LANGS[lang].add_part(year, day, part, loggers=self.loggers[:-1], **kwargs)

                if lang_order:
                    self.print(f"{year}: Discovered {entity_name} in languages: {', '.join(l.title() for l in sorted(lang_data))}")

        def load_from_columns(entity_name: str):
            entity_path = map_to_entity_path(["**"])
            scalar_view = recording.view(index="Day", contents={entity_path: ["Scalar"]})
            if len(scalar_view.schema().index_columns()):
                columns = [c for c in scalar_view.schema().component_columns() if c.entity_path.count("/") == 3]
                scalar_table = scalar_view.select(columns=columns).read_pandas()
                
                for day, row in scalar_table.iterrows():
                    for data, col in zip(row, columns):
                        if data:
                            lang, part, year = col.entity_path.split("/")[1:]
                            year, part = map(int, re.findall(r"\d+", f"{year} {part}"))
                            if lang not in LANGS:
                                raise ValueError(f"Language {lang.title()} not found in available languages")
                            LANGS[lang].add_part(year, day + 1, part, loggers=self.loggers[:-1], **{entity_name: data[0]})

        if self.args.no_load or not (self.log_file and os.path.exists(self.log_file) and self.log_file.suffix == ".rrd"):
            return False
        
        self.print(f"Loading existing data from {self.log_file}")

        recording = rr.dataframe.load_recording(self.log_file)
        for logger in self.loggers:
            if not hasattr(logger, "name"):
                continue

            if hasattr(logger, "data_start"):
                load_from_table(logger.name, logger.data_start)
            else:
                load_from_columns(logger.name)

        self.active_recording.initialized_entities.clear()
        self.print("Loaded existing data")

        return True

    def log_everything(self, **kwargs):
        """
        Log everything
        """
        for lang in LANGS.values():
            for year in lang.years.values():
                self.log_year(year, entity_path=[lang.lang, year.year], **kwargs)

            rr.set_time_sequence("Day", 0, recording=self.active_recording.recording)
            self.log_lang(lang, entity_path=[lang.lang], **kwargs)

        for logger in self.loggers:
            if hasattr(logger, "format"):
                p_style, logger.format = logger.format, "MARKDOWN"
                self.text_log([logger.name], str(logger), media_type=rr.MediaType.MARKDOWN)
                logger.format = p_style

        if not getattr(self.args, "no_blueprint", False):
            rr.send_blueprint(load_blueprint(self.args.default_blueprint, blueprint_dir=self.blueprint_dir, loggers=self.loggers[:-1], **kwargs), recording=self.active_recording.recording)

    ### Main logging functions
    def log(self, log_from: Any, **kwargs):
        """
        Main logging function
        """
        entity_path = kwargs.get("entity_path", [])

        if not len(self.loggers):
            return

        # Send to a specific logger
        if isinstance(log_from, Day):
            assert entity_path, "Entity path must be provided for logging a day"
            self.log_day(log_from, **kwargs)

        if isinstance(log_from, Language):
            self.log_lang(log_from, **kwargs)

    ### Logging helper functions
    def log_lang(self, lang: Language, entity_path: list[str]=[], saving: bool=False, **kwargs) -> None:
        """
        Log the runtime data for a language
        """
        if not len(lang):
            return
        
        if self.active_recording.initialize(entity_path):
            self.clear_log(entity_path)
            rr.send_blueprint(load_blueprint(self.args.default_blueprint, blueprint_dir=self.blueprint_dir, loggers=self.loggers[:-1], **kwargs), recording=self.active_recording.recording, make_active=not saving, make_default=not saving)

        comb_times = [year.combined_time for year in sorted(lang.years.values(), key=lambda x: x.year)]
        self.bar_log(entity_path + ["tot"], comb_times, **kwargs)

        avg_times = [year.avg_time for year in sorted(lang.years.values(), key=lambda x: x.year)]
        self.bar_log(entity_path + ["avg"], avg_times, **kwargs)

    def log_year(self, year: Year, entity_path: list[str]=[], **kwargs) -> None:
        """
        Log the runtime data for a year
        """
        def log_times(e_path: list[str], times: list[float], days: list[int]):
            if len(times) == len(days):
                self.series_line_log(e_path, times, "Day", days, **kwargs)
            # self.clear_log(e_path, recursive=True)
            # for t, day in zip(times, days):
            #     self.series_line_log(e_path, t, "Day", day, **kwargs)

        if not len(year):
            return
        
        days = list(range(1, len(year) + 1))
        for part in range(2):
            times = [day.times[part] for day in year.days.values() if day.times[part]]
            log_times(entity_path[:-1] + [f"part{part + 1}", entity_path[-1]], times, days)

        times = [day.combined_time for day in year.days.values() if day.combined_time]
        log_times(entity_path, times, days)
    
    def log_day(self, day: Day, entity_path: list[str]=[], **kwargs) -> None:
        """
        Log the runtime data for a day
        """
        if not len(day):
            return

        for part in range(1, 3):
            if time := day.times[part - 1]:
                self.series_line_log(entity_path[:-2] + [f"part{part}", entity_path[-2]], time, "Day", day.day, **kwargs)
        
        if day.combined_time:
            self.series_line_log(entity_path[:-1], day.combined_time, "Day", day.day, **kwargs)

    ### Actual rerun logging functions
    def clear_log(self, entity_path: list[str], recursive: bool=False, **kwargs):
        """
        Clear a log
        """
        log_name = map_to_entity_path(entity_path)

        rr.log(log_name, rr.Clear(recursive=recursive), recording=self.active_recording.recording)
        self.print(f'Clearing {log_name}')

    def series_line_log(self, entity_path: list[str], data: float | list[float], seq_str: str, seq: int | list[int], **kwargs):
        """
        Log a value as a part of a time series line
        """
        assert type(data) != type(seq) or len(data) == len(seq), "Data and sequence must be the same length"

        log_name = map_to_entity_path(entity_path)

        extras = {"width": rr.components.StrokeWidth(5), "name": str(entity_path[-1]).title(), "aggregation_policy": rr.components.AggregationPolicy.Off}
        color = self.entity_color(entity_path)
        if color:
            extras["color"] = rr.components.Color(colors.to_rgba(color))

        if self.active_recording.initialize(entity_path):
            rr.log(log_name, rr.SeriesLine(**extras), recording=self.active_recording.recording, static=True)

        if isinstance(data, list):
            rr.disable_timeline(seq_str, recording=self.active_recording.recording)
            rr.send_columns(log_name, times=[rr.TimeSequenceColumn(seq_str, seq)], components=[rr.components.ScalarBatch(data)], recording=self.active_recording.recording)
        else:
            rr.set_time_sequence(seq_str, seq, recording=self.active_recording.recording)
            # rr.log(log_name, rr.Scalar(data), extras, recording=self.active_recording.recording)
            rr.log(log_name, rr.Scalar(data), recording=self.active_recording.recording)
            rr.set_time_sequence(seq_str, 0, recording=self.active_recording.recording)
        
        self.print(f'Logging series line for {log_name}')

    def series_point_log(self, entity_path: list[str], data: float, seq_str: str, seq: int, marker_size: int=5, **kwargs):
        """
        Log a value as a part of a time series with points
        """
        log_name = map_to_entity_path(entity_path)

        if self.active_recording.initialize(entity_path):
            self.clear_log(entity_path)

        rr.set_time_sequence(seq_str, seq, recording=self.active_recording.recording)
        rr.log(log_name, rr.Scalar(data), rr.SeriesPoint(color=colors.to_rgba(self.entity_color(entity_path)), marker="Circle", marker_size=marker_size, **kwargs), recording=self.active_recording.recording)
        rr.set_time_sequence(seq_str, 0, recording=self.active_recording.recording)
        self.print(f'Logging series point for {log_name}')

    def bar_log(self, entity_path: list[str], data: list[float], **kwargs):
        """
        Log a set of values as a bar chart
        """
        if len(data) < 2:
            return

        log_name = map_to_entity_path(entity_path)

        extras = []
        color = self.entity_color(entity_path)
        if color:
            extras.append(rr.components.Color(colors.to_rgba(color)))

        if self.active_recording.initialize(entity_path):
            self.clear_log(entity_path)
        rr.log(log_name, rr.BarChart(data), extras, recording=self.active_recording.recording)
        self.print(f'Logging bar chart for {log_name}: {data}')

    def text_log(self, entity_path: list[str], text: str | list[str], **kwargs):
        """
        Log some text
        """
        log_name = map_to_entity_path(entity_path)
        self.active_recording.initialize(entity_path)

        self.clear_log(entity_path)
        if isinstance(text, list):
            text = "\n".join(text)
        rr.log(log_name, rr.TextDocument(text, **kwargs), recording=self.active_recording.recording)
        self.print(f'Logging text for {log_name}')

    ### Helper functions for logging
    def entity_color(self, entity_path: list[str]) -> Optional[str]:
        """
        Set the color of the entity based on the last part of the path that has a color
        """
        ### Assemble the current entity colors
        entity_path = list(map(str, entity_path))
        years = set()
        for i, l in enumerate(sorted(LANGS.keys())):
            self.colormap[l] = COLOR_MAP(i % COLOR_MAP.N)
            years.update(LANGS[l].years.keys())

        for i, y in enumerate(sorted(years)):
            self.colormap[str(y)] = COLOR_MAP(i % COLOR_MAP.N)

        # Get the color of the last part of the entity path that has a color
        for p in entity_path[::-1]:
            if p in self.colormap:
                if 'avg' in entity_path:
                    return colors.to_rgba(self.colormap[p], alpha=0.5)
                return self.colormap[p]
