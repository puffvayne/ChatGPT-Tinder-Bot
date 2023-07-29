import pathlib
import sys

# add project directory to path
curr_file_path = pathlib.Path(__file__).absolute()
CURR_DIR = curr_file_path.parent
PROJECT_DIR = CURR_DIR.parent
sys.path.append(str(PROJECT_DIR))
print(f"[INFO] - append directory to path: {PROJECT_DIR}")

import json
import time
from tqdm import tqdm
from tinder_bot.tinder import TinderAPI, ASK_HOOK_UP_MSG_LS

token = ''
tinder_api = TinderAPI(token)
print(tinder_api)

recs_ls = tinder_api.get_recommendations()
for rec in recs_ls:
    # if rec.is_valid_so and rec.is_girl and rec.is_near:
    if rec.is_valid_so and rec.is_near:
        print(rec)
        print(rec.sexual_orientations)
        print()
