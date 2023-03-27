from typing import List
from .file_tool import read_file_lines_to_ls


def get_whitelist(fp) -> List:
    str_ls = read_file_lines_to_ls(fp)
    whitelist = [s.split(' # ')[0] for s in str_ls]
    return whitelist


def print_whitelist(fp):
    for s in read_file_lines_to_ls(fp):
        print(s)
