import pathlib
from typing import NamedTuple

class ArgumentError(Exception):
    def __init__(self, message: str, usage: str) -> None:
        self.USAGE = usage
        super().__init__(message)

    # ??
    # def __str__(self):
    #     return self.USAGE + "\n" + self.message
    
    # ?
    def __format__(self):
        print(self.USAGE)
        print(self.message)

class Config(NamedTuple):
    file_path: str

def file_ext(file_path: str) -> str:
    """Returns file extension."""
    return pathlib.Path(file_path).suffix