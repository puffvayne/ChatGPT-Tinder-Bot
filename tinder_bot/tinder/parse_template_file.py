import pathlib
from typing import Union, List


def read_file_lines_to_ls(fp: Union[pathlib.Path, str], encoding='utf-8') -> List:
    with open(fp, 'r', encoding=encoding) as f:
        return [line.rstrip() for line in f.readlines()]
