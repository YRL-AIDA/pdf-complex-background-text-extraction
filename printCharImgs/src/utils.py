import re
import warnings
from pathlib import Path


warnings.warn("rewrite remove_ext")
def get_project_root() -> Path:
    return Path(__file__).parent.parent


junkstring = "_junkstring"

def append_junk(string, counter):
    return f'{string}{junkstring}{counter}'

def remove_junk(string):
    return re.sub(r'_junkstring\d*', '', string)

def remove_ext(string):
    return string.split(".")[0]
