"""
Answer logger for Advent of Code
"""

import argparse
from dataclasses import dataclass, field
from functools import reduce
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import cv2
import numpy as np
import prettytable as pt
import pytesseract
from advent_of_code_ocr import convert_6
from PIL import Image, ImageDraw

from ..languages import LANGS
from . import LogCTX, Logger, LoggerAction


def convert_ans(ans: Any) -> str:
    """
    Convert answer to a readable format
    """
    if not isinstance(ans, str):
        ans = str(ans)

    if ans.count("\n") <= 1:
        return ans
    
    assert(set(ans) == {"█", " ", "\n"})

    rows = [r for r in ans.split("\n") if r]
    min_ix = min(min(r.find("█") for r in rows) for r in rows)
    max_ix = max(max(r.rfind("█") for r in rows) for r in rows)
    rows = [r[min_ix:max_ix + 1] for r in rows]
    max_len = max(len(r) for r in rows)
    rows = [r.ljust(max_len) for r in rows]

    if len(rows) == 6:
        ans = convert_6("\n".join(rows), fill_pixel="█", empty_pixel=" ")
    else:
        # Do Optical Character Recognition
        ### BE AMAZED IF THIS WORKS ###
        img = Image.new("RGB", (len(rows[0]) + 2, len(rows) + 2), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        char_in_col = set(range(len(rows[0]) + 2))
        for y, row in enumerate(rows, 1):
            for x, c in enumerate(row, 1):
                if c == "█":
                    draw.point((x, y), (0, 0, 0))
                    if x in char_in_col:
                        char_in_col.remove(x)
                else:
                    draw.point((x, y), (255, 255, 255))
        
        ans = ""
        left_side = 0
        for right_side in sorted(char_in_col)[1::2]:
            temp_img = img.crop((left_side, 0, right_side + 1, len(rows) + 2))
            for _ in range(4):
                temp_img = temp_img.resize((temp_img.width * 2, temp_img.height * 2), Image.LANCZOS)
                temp_img = np.array(temp_img)
                temp_img = cv2.GaussianBlur(np.array(temp_img), (3, 3), 0)
                norm_img = np.zeros((temp_img.shape[0], temp_img.shape[1]), np.uint8)
                temp_img = cv2.normalize(temp_img, norm_img, 0, 255, cv2.NORM_MINMAX)
                temp_img = cv2.threshold(temp_img, 150, 255, cv2.THRESH_BINARY)[1]
                temp_img = Image.fromarray(temp_img)

            ans += pytesseract.image_to_string(temp_img, config="--psm 6").strip().upper()
            left_side = right_side + 1
    
    return ans


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

    def log(self, *args, **kwargs) -> None:
        """
        Log an answer
        """
        with LogCTX(self, kwargs):
            if not kwargs.get("log_all", False):
                self.log_part(*args, **kwargs)

    def log_part(self, year: int, day: int, part: int, *args, ans: Optional[str]=None, lang: Optional[str]=None, **kwargs) -> None:
        """
        Log an answer for a part
        """
        if not all((ans, lang, year, day, part)):
            raise ValueError("Answer, Language, year, day, and part must be provided for answer logging")

        try:
            ans = convert_ans(ans)
        except AssertionError:
            raise AssertionError(f"Invalid answer for {year} day {day} part {part} in {lang}")

        answer_table = self.answer_data
        for table_ix in [year, day, part]:
            if table_ix not in answer_table:
                answer_table[table_ix] = {}
            answer_table = answer_table[table_ix]

        answer_table[lang] = ans
        self.new_data.append((year, day, part, lang, ans))

    def get_tables(self, new_only: bool=False, **kwargs) -> List[Tuple[int, pt.PrettyTable]]:
        """
        Get answer tables
        """
        def add_answers(data: dict[Any], new_labels: dict={}) -> str:
            for ix, (lang, ans) in enumerate(sorted(data.items(), key=lambda x: x[0])):
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
                if not new_only or (year, day) in LANGS[lang].changed:
                    incorrect_table.add_row([year, day, part, lang.title(), correct, self.answer_data[year][day][part][lang]])
            if len(incorrect_table._rows):
                tables.append(("Incorrect", incorrect_table))

        changed = reduce(lambda x, y: x.union(y), [lang.changed for lang in LANGS.values()], set())
        for year, year_data in sorted(self.answer_data.items(), key=lambda x: x[0]):
            if not year_data:
                continue

            year_table = pt.PrettyTable(**kwargs)
            columns = {"Day": []}
            for day, day_data in sorted(year_data.items(), key=lambda x: x[0]):
                if not day_data or (new_only and (year, day) not in changed):
                    continue

                for part, part_data in sorted(day_data.items(), key=lambda x: x[0]):
                    if not any(map(lambda a: a is not None and len(a), part_data.values())):
                        continue

                    add_answers(part_data, {"Day": f"{day}" if part == 1 else ""})                        
            
            if len(columns["Day"]) == 0:
                continue
            
            for col_label, col_data in columns.items():
                while len(col_data) < max(map(len, columns.values())):
                    col_data.append("")
                year_table.add_column(col_label.title().center(5), col_data)

            tables.append((str(year), year_table))

        if s := kwargs.get("style", False):
            for _, year_table in tables:
                year_table.set_style(s)

        return tables

    def get_incorrect(self) -> Dict[Tuple[Any,], str]:
        """
        Get incorrect answers
        """
        # Load correct answers
        with open(Path(Path(__file__).parent.parent.parent, "aoc_answers.txt"), "r", encoding="utf-8") as f:
            correct_answers = {k: v for line in f.readlines() for k, v in [line.strip().split(": ")]}

        incorrect = {}
        for year_day, answers in correct_answers.items():
            year, day = map(int, year_day.split("-"))
            for part, correct in enumerate(answers.split(";"), 1):
                for lang, ans in self.answer_data.get(year, {}).get(day, {}).get(part, {}).items():
                    if ans and ans != correct:
                        incorrect[(year, day, part, lang)] = correct

        return incorrect
