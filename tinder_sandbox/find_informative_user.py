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
from src.utils.file_tool import to_json

token = 'f0a4c549-fcf0-404d-a56f-e5825c4b2dfe'
tinder_api = TinderAPI(token)
print(tinder_api)

res = list()
for _ in tqdm(range(15)):
    rec_ls = tinder_api.get_recommendations()
    for rec in rec_ls:
        user_info_json = tinder_api.get_user_info_json(rec.id)
        if user_info_json['status'] == 200:
            r = user_info_json['results']
            res.append(r)
            print(len(r.keys()))

# sort res's element with elements's key count, the element with most keys should be at index 0
res = sorted(res, key=lambda x: len(x.keys()), reverse=True)
print(len(res[0].keys()))
to_json(res, 'user_infos.json')
