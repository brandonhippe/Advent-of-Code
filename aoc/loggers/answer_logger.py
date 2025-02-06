"""
Answer logger for Advent of Code
"""

import argparse
from collections import defaultdict
from dataclasses import dataclass, field
import os
from pathlib import Path
from typing import Any, Dict, Hashable, List, Optional, Tuple

import cv2
import numpy as np
import pytesseract
from advent_of_code_ocr import convert_6
from PIL import Image, ImageDraw

from ..languages import LANGS, Language, get_released
from ..utils.aoc_web import AOC_COOKIE, get_answers, submit_answer
from . import Logger, LoggerAction, DataTracker


@dataclass
class AnswerTracker(DataTracker):
    """
    Track answer data
    """

    # types: Dict[type, int] = field(default_factory=lambda: defaultdict(int))

    def add_data(self, key: Tuple[Hashable], *args, new_data: Any, incorrect: bool=False, **kwargs) -> None:
        super().add_data(key, *args, new_data=new_data, **kwargs)
        if incorrect:
            if "incorrect" not in self.data:
                self.data["incorrect"] = type(self)(False)
            self.data["incorrect"].add_data((key,), new_data=new_data)
        
        # if len(key) == 1 and key[0] not in self.types:
        #     self.types[key[0]] = type(new_data).__name__
    
    def update(self):
        """
        Convert answer to a readable format
        """
        for k, ans in self.data.items():
            if isinstance(ans, type(self)):
                # for t, count in ans.types.items():
                #     if isinstance(count, int):
                #         self.types[t] += count
                #     else:
                #         self.types[count] += 1

                continue

            if not isinstance(ans, str):
                ans = str(ans)

            if ans.count("\n") > 1:
                assert set(ans) == {"█", " ", "\n"}

                rows = [r for r in ans.split("\n") if r]
                min_ix = min(min(r.find("█") for r in rows) for r in rows)
                max_ix = max(max(r.rfind("█") for r in rows) for r in rows)
                rows = [r[min_ix : max_ix + 1] for r in rows]
                max_len = max(len(r) for r in rows)
                rows = [r.ljust(max_len) for r in rows]

                if len(rows) == 6:
                    ans = convert_6("\n".join(rows), fill_pixel="█", empty_pixel=" ")
                else:
                    # Do Optical Character Recognition
                    ### BE AMAZED IF THIS WORKS ###
                    img = Image.new(
                        "RGB", (len(rows[0]) + 2, len(rows) + 2), (255, 255, 255)
                    )
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
                        temp_img = img.crop(
                            (left_side, 0, right_side + 1, len(rows) + 2)
                        )
                        for _ in range(4):
                            temp_img = temp_img.resize(
                                (temp_img.width * 2, temp_img.height * 2), Image.LANCZOS
                            )
                            temp_img = np.array(temp_img)
                            temp_img = cv2.GaussianBlur(np.array(temp_img), (3, 3), 0)
                            norm_img = np.zeros(
                                (temp_img.shape[0], temp_img.shape[1]), np.uint8
                            )
                            temp_img = cv2.normalize(
                                temp_img, norm_img, 0, 255, cv2.NORM_MINMAX
                            )
                            temp_img = cv2.threshold(
                                temp_img, 150, 255, cv2.THRESH_BINARY
                            )[1]
                            temp_img = Image.fromarray(temp_img)

                        ans += (
                            pytesseract.image_to_string(temp_img, config="--psm 6")
                            .strip()
                            .upper()
                        )
                        left_side = right_side + 1

            self.data[k] = ans

    def keys_to_indecies(self, keys: List[Hashable]) -> Optional[Tuple[List[str], List[Any], int]]:
        *keys, k = keys
        if isinstance(k, tuple):
            col_name, *row_indecies = k
            tab_name = keys[-1]
        elif len(keys) < 2:
            col_name = str(k)
            tab_name = f"Data"
            row_indecies = keys
        else:
            col_name, tab_name, *row_indecies = keys[-3:] + [k]

        if isinstance(k, tuple):
            return (col_name, tab_name, *row_indecies), (False, False, True, slice(-1)), len(keys)
        else:
            return (col_name, tab_name, *row_indecies),  (True, True, False, slice(-1)), len(keys)


@dataclass
class AnswerLogger(Logger):
    """
    Answer logger for Advent of Code
    """

    data: AnswerTracker = field(default_factory=AnswerTracker)
    incorrect: AnswerTracker= field(default_factory=lambda: AnswerTracker(False))
    name: str = "answers"
    data_start: int = 2
    value_key: str = "ans"
    table_style: str = "DOUBLE_BORDER"
    correct_answers: Dict[Tuple[int, int, int], str] = field(default_factory=dict)
    correct_changed: bool = False
    correct_answers_path = Path(Path(__file__).parent, "correct_answers", f"{AOC_COOKIE}_answers.txt")
    data_prefix: str = AOC_COOKIE

    @staticmethod
    def add_arguments(parser: argparse.ArgumentParser) -> None:
        """
        Add arguments to the parser
        """
        parser.add_argument(
            "--answers",
            "-a",
            action=LoggerAction,
            nargs="*",
            help='Log answers. Add " verbose" or "v" to run in verbose mode',
            type=AnswerLogger,
        )
        parser.add_argument(
            "--no-load",
            action="store_true",
            help="Don't load existing advent of code data",
        )
        parser.add_argument(
            "--no-save", action="store_true", help="Don't save advent of code data"
        )
        parser.add_argument(
            "--answers-table-style", type=str, choices=["DEFAULT", "SINGLE_BORDER", "DOUBLE_BORDER"], help="Style of the answer table"
        )

    ### Context manager functions
    def __enter__(self):
        # Load correct answers
        if os.path.exists(self.correct_answers_path):
            with open(
                self.correct_answers_path, "r", encoding="utf-8"
            ) as f:
                self.correct_answers = {
                    tuple([*map(int, k.split("-")), i]): ans
                    for line in f.readlines()
                    for k, v in [line.strip().split(": ")]
                    for i, ans in filter(lambda ans: len(ans[1]), enumerate(v.split(";"), 1))
                }

        # for year in get_released():
        #     for day in get_released(year):
        #         if any((year, day, i) not in self.correct_answers for i in ([1] if day == 25 else [1, 2])):
        #             for part, ans in get_answers(year, day).items():
        #                 self.correct_answers[(year, day, part)] = ans
        #                 self.correct_changed = True

        super().__enter__()
        self.changed_data = AnswerTracker(False)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if super().__exit__(exc_type, exc_val, exc_tb):
            if self.correct_changed:
                self.correct_answers_path.parent.mkdir(parents=True, exist_ok=True)
                with open(
                    Path(self.correct_answers_path), "w", encoding="utf-8"
                ) as f:
                    for year in get_released():
                        for day in get_released(year):
                            answers = f"{self.correct_answers.get((year, day, 1), ' ')};{self.correct_answers.get((year, day, 2), ' ')}"
                            f.write(f"{year}-{day}: {answers}\n")
        
        return not bool(exc_type)

    def log(self, *args, **kwargs) -> None:
        """
        Log an answer
        """

        def prep_dict_log(d: dict, *args) -> None:
            if not any(isinstance(v, dict) for v in d.values()):
                x_data = sorted(d.keys())
                y_data = [d[k] for k in x_data]
                if len(args) == 3:
                    if isinstance(args[2], int):
                        self.add_new_data(
                            args[1],
                            x_data,
                            args[2],
                            args[0],
                            lang=args[0],
                            **{self.value_key: y_data}
                        )
                    else:
                        self.add_new_data(
                            args[1],
                            x_data,
                            args[0],
                            lang=args[0],
                            **{self.value_key: y_data}
                        )
                elif len(args) == 2:
                    self.add_new_data(
                        x_data,
                        args[0],
                        args[1],
                        lang=args[0],
                        **{self.value_key: y_data}
                    )

                return

            for k, v in d.items():
                if isinstance(v, dict):
                    prep_dict_log(d[k], *args, k)
                else:
                    pass

        if not kwargs.get("log_all", False):
            self.log_part(*args, **kwargs)
        else:
            data = defaultdict(lambda: defaultdict(dict))
            for year, day in self.runtime_days(new_only=False):
                for lang in LANGS:
                    if [lang, year, day] not in self.data:
                        continue

                    if year not in data[lang]:
                        data[lang][year] = defaultdict(
                            lambda: defaultdict(dict), {"combined": {}}
                        )

                    for part in [1, 2]:
                        if [lang, year, day, part] in self.data:
                            data[lang][year][part][day] = self.data[
                                lang, year, day, part
                            ]

                    data[lang][year]["combined"][day] = ""

            prep_dict_log(data)

        super().log(*args, **kwargs)

    def log_part(
        self,
        year: int,
        day: int,
        part: int,
        lang: Optional[Language] = None,
        ans: Optional[str] = None,
        event: Optional[str]="on_log",
        **kwargs
    ) -> None:
        """
        Log an answer for a part
        """
        if not all((ans, lang, year, day, part)):
            raise ValueError(
                "Answer, Language, year, day, and part must be provided for answer logging"
            )

        incorrect = False
        self.data.add_data((lang, year, day, part), new_data=ans)
        if (ans := self.data[lang, year, day, part]) != self.correct_answers.get((year, day, part), ans) and ans != "":
            self.data.add_data((lang, year, day, part), new_data=ans, incorrect=True)
            incorrect = True

        if event == "on_log":
            self.changed_data.add_data((lang, year, day, part), new_data=ans, incorrect=incorrect)

        self.add_new_data(
            year, day, part, lang, ans=ans
        )

        if (year, day, part) not in self.correct_answers:
            if submit_answer(year, day, part, ans):
                self.correct_answers[(year, day, part)] = ans
                self.correct_changed = True

    def get_incorrect(self, new_only: bool = False) -> Dict[Tuple[Any,], str]:
        """
        Get incorrect answers
        """
        incorrect = {}
        for year, day in self.runtime_days(new_only):
            for lang in filter(lambda l: l in self.data, LANGS):
                for part, correct in enumerate(self.correct_answers[(year, day)], 1):
                    if (day, part) == (25, 2):
                        continue

                    if [year, day, part] in self.data[
                        lang
                    ] and self.data[lang, year, day, part] != correct:
                        incorrect[(year, day, part, lang)] = (
                            correct,
                            self.data[(lang, year, day, part)],
                        )

        return incorrect
