"""
Rerun viewer for profiled AOC code
"""

import argparse
import os
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional
from uuid import uuid4

import rerun as rr

from ..loggers import Logger
from ..languages import get_released
from . import Viewer, ViewerAction, map_to_entity_path
from .blueprints import *


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
class RerunViewer(Viewer):
    """
    Class to handle runtime data for Advent of Code solutions\\
    Displays the data in a rerun viewer
    """
    application_id: str = "Advent of Code"
    bar_graph_data: dict = field(default_factory=lambda: defaultdict(lambda: defaultdict(lambda: {y: 0 for y in get_released()})))
    blueprint_dir: Path = Path(Path(__file__).parent, "blueprints")
    name: str = "rerun"

    @staticmethod
    def add_arguments(parser: argparse.ArgumentParser):
        """
        Add arguments to the parser
        """
        parser.add_argument("--rerun", action=ViewerAction, nargs="*", help='Run the rerun viewer. Add " verbose" to run in verbose mode', type=RerunViewer)
        
        parser.add_argument("--default-blueprint", type=str, default=Path(Path(__file__).parent, "blueprints", "main.yml"), help="Path to yaml that defines the base level blueprint")
        parser.add_argument("--no-blueprint", action="store_true", help="Don't load any blueprints")

        rr.script_add_args(parser)

    def start_viewer(self, **kwargs):
        """
        Start the rerun viewer
        """

        self.active_recording = RecordingWithInitialized(application_id=self.application_id, make_default=True, make_thread_default=True)
        rr.init(application_id=self.application_id, spawn=True, recording_id=self.active_recording.uuid)
        rr.set_time_sequence("Day", 0, recording=self.active_recording.recording)

        self.log_everything(**kwargs)

    ### Context manager functions
    def __enter__(self) -> 'RerunViewer':
        """
        Setup the rerun viewer
        """
        super().__enter__() 
        self.start_viewer()
        
        self.p_verbose = self.args.verbose
        self.verbose = False

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """
        Exit, spawning the rerun viewer if no errors occurred
        """
        if super().__exit__(exc_type, exc_val, exc_tb):
            self.verbose = self.p_verbose
            
            self.start_viewer(load_data=False, on_exit_from=type(self))
            self.print("Finished logging to rerun viewer")

        rr.script_teardown(self.args)
        return bool(exc_type)

    ### Logging helper functions
    def log_everything(self, loggers: Optional[list[Logger]]=None, **kwargs):
        """
        Log everything
        """
        for logger in loggers or self.loggers:
            logger.log(log_all=True, **kwargs)
            if hasattr(logger, "format"):
                p_style, logger.format = logger.format, "MARKDOWN"
                self.text_log([logger.name], str(logger), media_type=rr.MediaType.MARKDOWN)
                logger.format = p_style

        if not getattr(self.args, "no_blueprint", False):
            rr.send_blueprint(load_blueprint(self.args.default_blueprint, blueprint_dir=self.blueprint_dir, loggers=self.loggers, **kwargs), recording=self.active_recording.recording)

    def log_year_avg_tot(self, time: float | list[float], year: int | list[int], lang: str, plot: str, **kwargs) -> None:
        """
        Log the average/total runtime data for a year
        """
        if not time:
            return
        
        assert type(time) != type(year) or len(time) == len(year), "Data and sequence must be the same length"

        self.new_bp(lang, **kwargs)
        if not isinstance(year, list):
            time = [time] 
            year = [year]
        
        for y, t in zip(year, time):
            self.bar_graph_data[plot][lang][y] = t

        data = list(map(lambda x: x[1], sorted(self.bar_graph_data[plot][lang].items(), key=lambda x: x[0])))
        self.bar_log([lang, plot], data, **kwargs)
    
    def log_day(self, time: float | list[float], year: int, day: int, lang: str, **kwargs) -> None:
        """
        Log the runtime data for a day
        """
        if not time:
            return

        self.new_bp(lang, **kwargs)
        self.series_line_log([lang, year], time, "Day", day, **kwargs)

    def log_part(self, time: float | list[float], year: int, day: int | list[int], part: int, lang: str, **kwargs):
        """
        Log the runtime data for a part
        """
        if not time:
            return

        self.new_bp(lang, **kwargs)
        self.series_line_log([lang, f"part{part}", year], time, "Day", day, **kwargs)

    ### Actual rerun logging functions
    def new_bp(self, lang: str, **kwargs):
        if self.active_recording.initialize([lang]):
            self.clear_log([lang])
            rr.send_blueprint(load_blueprint(self.args.default_blueprint, blueprint_dir=self.blueprint_dir, loggers=self.loggers, **kwargs), recording=self.active_recording.recording)

    def clear_log(self, entity_path: list[str], recursive: bool=False, **kwargs):
        """
        Clear a log
        """
        log_name = map_to_entity_path(entity_path)

        rr.log(log_name, rr.Clear(recursive=recursive), recording=self.active_recording.recording)
        # self.print(f'Clearing {log_name}')

    def series_line_log(self, entity_path: list[str], data: float | list[float], seq_str: str, seq: int | list[int], **kwargs):
        """
        Log a value as a part of a time series line
        """
        assert type(data) != type(seq) or len(data) == len(seq), "Data and sequence must be the same length"

        log_name = map_to_entity_path(entity_path)

        extras = {"width": rr.components.StrokeWidth(5), "name": str(entity_path[-1]).title(), "aggregation_policy": rr.components.AggregationPolicy.Off}
        color = self.entity_color(entity_path)
        if color:
            extras["color"] = rr.components.Color(color)

        if self.active_recording.initialize(entity_path):
            rr.log(log_name, rr.SeriesLine(**extras), recording=self.active_recording.recording, static=True)

        if isinstance(data, list):
            rr.disable_timeline(seq_str, recording=self.active_recording.recording)
            rr.send_columns(log_name, times=[rr.TimeSequenceColumn(seq_str, seq)], components=[rr.components.ScalarBatch(data)], recording=self.active_recording.recording)
        else:
            rr.set_time_sequence(seq_str, seq, recording=self.active_recording.recording)
            rr.log(log_name, rr.Scalar(data), recording=self.active_recording.recording)

        rr.set_time_sequence(seq_str, 0, recording=self.active_recording.recording)        
        # self.print(f'Logging series line for {log_name}')

    def series_point_log(self, entity_path: list[str], data: float, seq_str: str, seq: int, marker_size: int=5, **kwargs):
        """
        Log a value as a part of a time series with points
        """
        log_name = map_to_entity_path(entity_path)

        if self.active_recording.initialize(entity_path):
            self.clear_log(entity_path)

        rr.set_time_sequence(seq_str, seq, recording=self.active_recording.recording)
        rr.log(log_name, rr.Scalar(data), rr.SeriesPoint(color=self.entity_color(entity_path), marker="Circle", marker_size=marker_size, **kwargs), recording=self.active_recording.recording)
        rr.set_time_sequence(seq_str, 0, recording=self.active_recording.recording)
        # self.print(f'Logging series point for {log_name}')

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
            extras.append(rr.components.Color(color))

        if self.active_recording.initialize(entity_path):
            self.clear_log(entity_path)
        rr.log(log_name, rr.BarChart(data), extras, recording=self.active_recording.recording)
        # self.print(f'Logging bar chart for {log_name}: {data}')

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
        # self.print(f'Logging text for {log_name}')
