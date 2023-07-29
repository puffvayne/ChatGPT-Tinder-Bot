# coding: utf-8
"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 6/18/23
"""
from typing import Any
from rich.console import Console

from . import styles as STYLE


class RichPrinter:
    def __init__(self):
        self.rich_console = Console()

    def __call__(self, msg: Any, style: str = STYLE.DEFAULT):
        self.print(msg, style)

    def print(self, msg: Any, style: str = STYLE.DEFAULT):
        self.rich_console.print(msg, style=style)
