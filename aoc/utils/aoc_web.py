"""
Utility functions for interacting with the Advent of Code website
"""

import os

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()


def get_input(year: int, day: int, *args, **kwargs) -> str:
    """
    Get the input for a given year and day from the Advent of Code website
    """
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    aoc_cookie = os.getenv("AOC_COOKIE", "")
    assert aoc_cookie, "No AOC_COOKIE found in environment variables"

    response = requests.get(url, cookies={"session": aoc_cookie})

    if response.status_code == 200:
        return BeautifulSoup(response.content, 'html.parser').text
    else:
        raise FileNotFoundError(f"Error: {response.status_code} for {url=}")
