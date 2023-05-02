import pathlib
from importlib.resources import read_text

# >>>>>> Global Variables >>>>>>
TINDER_URL = 'https://api.gotinder.com'
PKG_ROOT_DIR = pathlib.Path(__file__).absolute().parent
TEMPLATE_DIR = PKG_ROOT_DIR / 'template'


def __get_hook_up_msg_ls():
    from .parse_template_file import read_file_lines_to_ls
    return [read_file_lines_to_ls(fp) for fp in (TEMPLATE_DIR / 'hook_up_msg').iterdir()]


ASK_HOOK_UP_MSG_LS = __get_hook_up_msg_ls()

# <<<<<< Global Variables <<<<<<

# Class of Modules
from .person import Person
from .profile import Profile
from .tinder_api import TinderAPI
