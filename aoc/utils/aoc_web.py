"""
Utility functions for interacting with the Advent of Code website
"""

import os
import re
from typing import Dict

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
AOC_COOKIE = os.getenv("AOC_COOKIE", "")
assert AOC_COOKIE, "No AOC_COOKIE found in environment variables"


def get_from_url(url: str) -> BeautifulSoup:
    """
    Get the content of a given URL
    """
    response = requests.get(url, cookies={"session": AOC_COOKIE}, timeout=5)

    if response.status_code == 200:
        return BeautifulSoup(response.content, 'html.parser')
    else:
        raise FileNotFoundError(f"Error: {response.status_code} for {url=}")


def get_input(year: int, day: int, *args, **kwargs) -> str:
    """
    Get the input for a given year and day from the Advent of Code website
    """
    return get_from_url(f"https://adventofcode.com/{year}/day/{day}/input").text


def get_answers(year: int, day: int, *args, **kwargs) -> Dict[int, str]:
    """
    Get the answers for a given year and day from the Advent of Code website
    """
    soup = get_from_url(f"https://adventofcode.com/{year}/day/{day}")
    
    part_answers = {}
    for part, ans_str in enumerate(filter(None, map(lambda p: re.search(r"^Your puzzle answer was (.+)\.$", p.text), soup.find_all("p"))), 1):
        part_answers[part] = ans_str.group(1)

    return part_answers
