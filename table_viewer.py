"""
Command Line Interface Viewer for Advent of Code data
"""

import argparse
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Generator, Iterable, Optional, Tuple, List, Dict

import prettytable as pt

from ..languages import Language, LANGS
from ..loggers import Logger
from . import Viewer


@dataclass
class TableMaker:
    """
    Make a table from logged data
    """

    index_columns: List
    columns: Dict[str, List[Any]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.columns = defaultdict(list, {c: [] for c in self.index_columns})

    def __call__(
        self, reduce_repeats: bool = True, add_dividers: bool = True, **kwargs
    ) -> pt.PrettyTable:
        max_len = max(map(len, self.columns.values()))
        for col in self.columns.values():
            col.extend([""] * (max_len - len(col)))

        row_data = defaultdict(list)
        dividers = set()
        for col_name in self.index_columns + sorted(
            filter(lambda k: k not in self.index_columns, self.columns.keys())
        ):
            data = self.columns[col_name]
            col_title = str(col_name).center(5).title()
            if col_name in self.index_columns:
                p_data = None
                reduced_data = []
                for d in data:
                    if not reduce_repeats or p_data is None or p_data != d:
                        if len(reduced_data) and not len(reduced_data[-1]):
                            dividers.add(len(reduced_data))

                        reduced_data.append(d)
                        p_data = d
                    else:
                        reduced_data.append("")
            else:
                reduced_data = data

            row_data[0].append(col_title)
            for i, row in enumerate(reduced_data, 1):
                row_data[i].append(row)

        table = pt.PrettyTable(field_names=row_data[0], **kwargs)
        for i, row in sorted(row_data.items(), key=lambda x: x[0]):
            if not row or not i:
                continue

            table.add_row(row, divider=add_dividers and i in dividers)

        return table

    def add_data(self, data: Any, col_name: str, index_labels: Dict[str, str]) -> str:
        assert set(index_labels.keys()) == set(
            self.index_columns
        ), "Index labels must match index columns"

        if not (data := self.table_str(data)):
            return

        min_len = min(len(self.columns[c]) for c in self.index_columns)
        ix = 0
        while ix < min_len and any(
            self.columns[col][ix] != index_labels[col] for col in index_labels
        ):
            ix += 1

        for col, str in [(col_name, data)] + list(index_labels.items()):
            if len(self.columns[col]) > ix:
                continue

            while len(self.columns[col]) <= ix:
                self.columns[col].append("")
            self.columns[col][-1] = str

    def del_col(self, col: str) -> None:
        """
        Delete a column from the table
        """
        if col not in self.columns:
            return

        if col in self.index_columns:
            self.index_columns.remove(col)
        del self.columns[col]

    def table_str(self, data: Any) -> str:
        """
        Convert data into the string used in the table
        """
        if isinstance(data, float):
            return f"{data:.4f}"
        return str(data)


@dataclass
class TableViewer():
    """
    View Advent of Code data in table(s)
    """

    args: argparse.Namespace
    name: str = "table"
    part_data: Dict[str, Dict[int, Dict[int, Dict[int, Any]]]] = field(
        default_factory=lambda: defaultdict(
            lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
        )
    )
    tables: Dict[str, Dict[int, TableMaker]] = field(
        default_factory=lambda: defaultdict(
            lambda: defaultdict(lambda: TableMaker(["Day", "Part"]))
        )
    )
    default: bool = True

    def __post_init__(self):
        if isinstance(self.args, argparse.Namespace):
            if self.name != "table":
                self.default = False

            vars(self.args).get(f"{self.name}_attachments", []).extend(
                vars(self.args).get(f"table_attachments", [])
            )
            self.format = vars(self.args).get(f"{self.name}_format", "DOUBLE_BORDER")
            super().__post_init__()

    @staticmethod
    def add_arguments(parser: argparse.ArgumentParser) -> None:
        """
        Add arguments to the parser
        """
        parser.add_argument(
            "--table-attachments",
            nargs="*",
            default=[Path(Path(__file__).parent, "table.yml")],
            help="Path to yaml file(s) that define the attachments for the Table Viewer",
        )
        parser.add_argument(
            "--table-format",
            type=str,
            default="DOUBLE_BORDER",
            help="Format of the table. Default: DOUBLE_BORDER",
        )

    ### Context manager functions
    def __exit__(self, exc_type, exc_val, exc_tb):
        if super().__exit__(exc_type, exc_val, exc_tb) and self.name == "table":
            pass
            # self.print(self())
        return not bool(exc_type)

    def __call__(
        self, from_logger: Optional[Logger] = None, del_keys: bool = False, **kwargs
    ) -> str:
        """
        Get tables for CLI/Markdown printing
        """

        def lower(s: str) -> str:
            return s.lower()

        def format_tables(
            **kwargs,
        ) -> Generator[Tuple[str, List[Tuple[str, pt.PrettyTable]]], None, None]:
            for k, v in kwargs.items():
                if hasattr(pt, v):
                    kwargs[k] = getattr(pt, v)

            for logger_name, logger_tables in filter(
                lambda k: from_logger is None or k[0] == from_logger.name,
                self.tables.items(),
            ):
                if logger_name in ["answers"]:
                    for table in logger_tables.values():
                        table.del_col("Part")

                if logger_name == "runtimes":
                    for year, table in logger_tables.items():
                        for lang in filter(
                            lambda l: year in self.part_data[logger_name].get(l, {}),
                            LANGS,
                        ):
                            table.add_data(
                                self.part_data[logger_name][lang][year]["avg"],
                                lang,
                                {"Day": "Average", "Part": ""},
                            )
                            if "tot" in self.part_data[logger_name][lang][year]:
                                table.add_data(
                                    self.part_data[logger_name][lang][year]["tot"],
                                    lang,
                                    {"Day": "Total", "Part": ""},
                                )

                logger_tables = [
                    (
                        str(year),
                        table(
                            reduce_repeats=isinstance(year, int),
                            add_dividers=self.format in ["DEFAULT"],
                            **kwargs,
                        ),
                    )
                    for year, table in logger_tables.items()
                ]

                if s := kwargs.get("style", False):
                    for _, table in logger_tables:
                        table.set_style(s)

                yield logger_name, logger_tables

        ret_str = ""
        for logger_name, tables in format_tables(style=self.format):
            if self.format.upper() == "MARKDOWN":
                md = f"# Advent of Code {logger_name.title()}\n\nYearly {logger_name} for all languages:\n\n"

                if tables:
                    for title_str, _ in tables:
                        md += f"* [{title_str}](#{'-'.join(map(lower, title_str.split()))})\n\n"

                    for title_str, year_table in tables:
                        md += f"\n## {title_str}\n\n"
                        md += f"[Back to top](#advent-of-code-{logger_name})\n\n"
                        md += year_table.get_string() + "\n"
                else:
                    md += "No data to display"

                ret_str += md
            else:
                ret_str += "\n\n" + "\n\n".join(
                    f"{year} {logger_name.title()}:\n{table}" for year, table in tables
                )

        if del_keys:
            del_loggers = [from_logger.name if from_logger else self.tables.keys()]
            for d in del_loggers:
                if d in self.tables:
                    del self.tables[d]
                if d in self.part_data:
                    del self.part_data[d]

        return ret_str

    def __lt__(self, other: object) -> bool:
        if self.name == "table":
            return False

        return super().__lt__(other)

    ### Viewing helper functions
    def clear(self, *args, event: str = "", verbose: bool=False, **kwargs) -> None:
        """
        Clear the viewer, printing the tables if necessary
        """
        assert len(event), "Event must be specified"
        self.print(f"{event}, clearing tables!")

        p_verbose, self.verbose = self.verbose, verbose
        table_str = self(del_keys=True, **kwargs)

        if not self.verbose and event in ["pre_exit"]:
            print(table_str)
        else:
            self.print(table_str)

        self.verbose = p_verbose

    def view_year(
        self,
        year: int | List[int],
        lang: Language,
        plot: str,
        from_logger: Logger,
        **kwargs,
    ) -> None:
        data_name = from_logger.value_key
        data = kwargs.get(data_name, None)
        if data is None:
            return

        for y, val in zip(*self.check_intypes(year, data)):
            self.part_data[from_logger.name][lang][y][plot] = val

    def view_day(
        self, year: int, day: int, lang: Language, from_logger: Logger, **kwargs
    ) -> None:
        data_name = from_logger.value_key
        data = kwargs.get(data_name, None)
        if data is None:
            return

        for d, val in zip(*self.check_intypes(day, data)):
            if len(self.part_data[from_logger.name][lang][year][d]) == 2:
                for part in [1, 2]:
                    self.tables[from_logger.name][year].add_data(
                        self.part_data[from_logger.name][lang][year][d][part],
                        lang,
                        {"Day": f"{d}", "Part": f"Part {part}"},
                    )
                self.tables[from_logger.name][year].add_data(
                    val, lang, {"Day": f"{d}", "Part": "Combined"}
                )

    def view_part(
        self,
        year: int,
        day: int | Iterable[int],
        part: int,
        lang: Language,
        from_logger: Logger,
        **kwargs,
    ) -> None:
        data_name = from_logger.value_key
        data = kwargs.get(data_name, None)
        if data is None:
            return

        for d, val in zip(*self.check_intypes(day, data)):
            self.part_data[from_logger.name][lang][year][d][part] = val
