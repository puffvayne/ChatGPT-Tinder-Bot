import pathlib
import sys

# add project directory to path
curr_file_path = pathlib.Path(__file__).absolute()
CURR_DIR = curr_file_path.parent
PROJECT_DIR = CURR_DIR.parent
sys.path.append(str(PROJECT_DIR))
print(f"[INFO] - append directory to path: {PROJECT_DIR}")

from src.tinder import TinderAPI, Person
from src.utils import to_json, read_json

token = ''
tinder_api = TinderAPI(token)
print(tinder_api)

# user_id = '630078929ca955010084b655'
# user_info_json = tinder_api.get_user_info_json(user_id)
# print(f"key len = {len(user_info_json['results'].keys())}")
# # print(user_info_json)
# p = Person(user_info_json['results'], tinder_api)

user_infos = read_json('user_infos.json')
for u in user_infos:
    # if u['teasers']:
        # print(u['teasers'])
    p = Person(u, tinder_api)
    print(p)
    # print()
    # break