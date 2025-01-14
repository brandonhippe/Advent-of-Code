"""
Answer logger for Advent of Code
"""

import argparse
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Tuple

import prettytable as pt

from .language_functions import Day
from .logger import Logger, LoggerAction


@dataclass
class AnswerLogger(Logger):
    """
    Answer logger for Advent of Code
    """
    answer_data: dict[Any, dict[Any, dict[Any, dict[Any, str]]]] = field(default_factory=dict)
    name: str = "answers"
    data_start: int = 2

    @staticmethod
    def add_arguments(parser: argparse.ArgumentParser) -> None:
        """
        Add arguments to the parser
        """
        parser.add_argument("--answers", "-a", action=LoggerAction, nargs="*", help='Log answers. Add " verbose" or "v" to run in verbose mode', type=AnswerLogger)

    def log(self, msg: Any, **kwargs) -> None:
        """
        Log an answer
        """
        if not isinstance(msg, Day):
            return
        
        entity_path = kwargs.get("entity_path", [])
        assert len(entity_path) >= 3, f"Entity path must be at least 3, not {len(entity_path)}"

        lang, year, day = entity_path[-3:]
        for part, ans in enumerate(msg.ans, 1):
            answer_table = self.answer_data
            for table_ix in [year, day, part]:
                if table_ix not in answer_table:
                    answer_table[table_ix] = {}
                answer_table = answer_table[table_ix]

            answer_table[lang] = ans

    def get_tables(self, **kwargs) -> List[Tuple[int, pt.PrettyTable]]:
        """
        Get answer tables
        """
        def add_answers(data: dict[Any], new_labels: dict={}) -> str:
            for ix, (lang, ans) in enumerate(data.items()):
                if not ans:
                    continue

                if lang not in columns:
                    columns[lang] = []

                while len(columns[lang]) < max(map(len, columns.values())):
                    columns[lang].append("")
                
                if ix == 0:
                    columns[lang].append("")
                
                columns[lang][-1] = ans

            for col, label in new_labels.items():
                while len(columns[col]) < max(map(len, columns.values())):
                    columns[col].append("")

                columns[col][-1] = label

        tables = []
        for k, v in kwargs.items():
            if hasattr(pt, v):
                kwargs[k] = getattr(pt, v)

        if incorrect := self.get_incorrect():
            incorrect_table = pt.PrettyTable()
            incorrect_table.field_names = ["Year", "Day", "Part", "Language", "Correct Answer", "Code Answer"]
            for (year, day, part, lang), correct in incorrect.items():
                incorrect_table.add_row([year, day, part, lang.title(), correct, self.answer_data[year][day][part][lang]])
            tables.append(("Incorrect", incorrect_table))

        for year, year_data in sorted(self.answer_data.items(), key=lambda x: x[0]):
            if not year_data:
                continue

            year_table = pt.PrettyTable(**kwargs)
            columns = {"Day": []}
            for day, day_data in sorted(year_data.items(), key=lambda x: x[0]):
                if not len(day_data):
                    continue

                for part, part_data in sorted(day_data.items(), key=lambda x: x[0]):
                    if not any(map(len, part_data.values())):
                        continue

                    add_answers(part_data, {"Day": f"{day}" if part == 1 else ""})                        
            
            for col_label, col_data in columns.items():
                while len(col_data) < max(map(len, columns.values())):
                    col_data.append("")
                year_table.add_column(col_label.title().center(5), col_data)

            tables.append((str(year), year_table))

        if "style" in kwargs:
            for _, year_table in tables:
                year_table.set_style(kwargs["style"])

        return tables

    def get_incorrect(self) -> Dict[Tuple[Any,], str]:
        """
        Get incorrect answers
        """
        # Load correct answers
        with open(Path(Path(__file__).parent.parent, "aoc_answers.txt"), "r", encoding="utf-8") as f:
            correct_answers = {k: v for line in f.readlines() for k, v in [line.strip().split(": ")]}

        incorrect = {}
        for year_day, answers in correct_answers.items():
            year, day = map(int, year_day.split("-"))
            for part, correct in enumerate(answers.split(";"), 1):
                for lang, ans in self.answer_data.get(year, {}).get(day, {}).get(part, {}).items():
                    if ans and ans != correct:
                        incorrect[(year, day, part, lang)] = correct

        return incorrect
