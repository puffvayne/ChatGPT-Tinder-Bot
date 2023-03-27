import pathlib
from src.ult import get_whitelist

PROJECT_DIR = pathlib.Path(__file__).absolute().parent

WHITELIST_PATH = PROJECT_DIR / 'whitelist.txt'

whitelist = get_whitelist(WHITELIST_PATH)
print(whitelist)