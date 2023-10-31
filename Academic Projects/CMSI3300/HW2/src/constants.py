"""
Constants to be used across various Ad Agent and Decision Network
tests, including network structure configurations and test file locations.

[!] Feel free to edit this file at will
[!] Note: any data frame in here should not be modified!
"""

import pandas as pd

# Lecture 5-2 Example
# -----------------------------------------------------------------------------------------
LECTURE_5_2_DATA = pd.read_csv("../dat/lecture5-2-data.csv")
LECTURE_5_2_STRUC = [("M", "C"), ("D", "C")]
LECTURE_5_2_DEC = ["D"]
LECTURE_5_2_UTIL = {"C": {0: 3, 1: 1}}

# AdBot Example
# -----------------------------------------------------------------------------------------
ADBOT_DATA = pd.read_csv("../dat/adbot-data.csv")
ADBOT_STRUC = [
    ("P", "T"),
    ("P", "G"),
    ("A", "T"),
    ("A", "F"),
    ("A", "H"),
    ("Ad1", "S"),
    ("Ad1", "G"),
    ("Ad2", "F"),
    ("F", "S"),
    ("G", "S"),
    ("H", "I"),
]
ADBOT_DEC = ["Ad1", "Ad2"]
ADBOT_UTIL = {"S": {0: 0, 1: 1776, 2: 500}}
