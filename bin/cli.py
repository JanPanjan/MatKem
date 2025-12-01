import pathlib
from typing import NamedTuple


class ArgumentError(Exception):
    def __init__(self, message: str, usage: str) -> None:
        super().__init__(message)
        print(f"\n{usage}\n")


class Config(NamedTuple):
    file_path: str


def file_ext(file_path: str) -> str:
    """Returns file extension."""
    return pathlib.Path(file_path).suffix
