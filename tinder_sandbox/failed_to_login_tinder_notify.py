import pathlib
import sys

# add project directory to path
curr_file_path = pathlib.Path(__file__).absolute()
CURR_DIR = curr_file_path.parent
PROJECT_DIR = CURR_DIR.parent
sys.path.append(str(PROJECT_DIR))
print(f"[INFO] - append directory to path: {PROJECT_DIR}")

import json
import os
from tinder_bot.utils import to_json
from tinder_bot.tinder import TinderAPI, ASK_HOOK_UP_MSG_LS
from tinder_bot.line import line_notify_message
from dotenv import load_dotenv

load_dotenv(PROJECT_DIR / 'local_settings/local.env')

TINDER_TOKEN = os.getenv('TINDER_TOKEN')


# def get_tinder_api():
#     try:
#         return TinderAPI(TINDER_TOKEN)
#     except Exception as e:
#         msg = f"Failed to login with TD api, might need to update token"
#         print(f"{msg}, Error: {e}")
#
#         line_notify_message(msg)
#
#
# tinder_api = get_tinder_api()
# print(f"tinder_api = {tinder_api}")
