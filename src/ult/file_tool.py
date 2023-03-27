from typing import List


def read_file_lines_to_ls(fp: str) -> List:
    with open(fp, 'r') as f:
        return [line.rstrip() for line in f.readlines()]


def str_ls_to_text_file(ls: List, fp: str):
    with open(fp, 'w') as f:
        for s in ls:
            f.write(str(s) + '\n')
