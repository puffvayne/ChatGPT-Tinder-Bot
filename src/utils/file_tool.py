import pathlib
import json
from argparse import Namespace
from typing import Union, List, Dict


def read_file_lines_to_ls(fp: str) -> List:
    with open(fp, 'r') as f:
        return [line.rstrip() for line in f.readlines()]


def str_ls_to_text_file(ls: List, fp: str):
    with open(fp, 'w') as f:
        for s in ls:
            f.write(str(s) + '\n')


def read_json(fp: Union[str, pathlib.Path]) -> Dict:
    return json.load(open(fp, 'r', encoding='utf-8'))


def to_json(data: Union[Dict, Namespace, List], fp: Union[str, pathlib.Path]):
    if isinstance(data, Namespace):
        data = vars(data)

    json.dump(data, open(fp, 'w', encoding='utf-8'), indent=4, ensure_ascii=False)
