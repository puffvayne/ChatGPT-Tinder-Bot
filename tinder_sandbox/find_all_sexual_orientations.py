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
from src.tinder import TinderAPI, ASK_HOOK_UP_MSG_LS

token = ''
tinder_api = TinderAPI(token)
print(tinder_api)

so = set()
for _ in tqdm(range(15)):
    recs_ls = tinder_api.get_recommendations()
    for rec in recs_ls:
        so.update(rec.sexual_orientations)
        time.sleep(1)
    print(so)

print('====')
print(so)
