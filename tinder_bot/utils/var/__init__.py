import pathlib

VAR_PKG_DIR = pathlib.Path(__file__).absolute().parent
UTILS_PKG_DIR = VAR_PKG_DIR.parent
PROJECT_ROOT_PKG_DIR = UTILS_PKG_DIR.parent
PROJECT_DIR = PROJECT_ROOT_PKG_DIR.parent

from . import log as LOG
