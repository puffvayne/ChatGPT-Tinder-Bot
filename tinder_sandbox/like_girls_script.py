import pathlib
import sys

# add project directory to path
curr_file_path = pathlib.Path(__file__).absolute()
CURR_DIR = curr_file_path.parent
PROJECT_DIR = CURR_DIR.parent
sys.path.append(str(PROJECT_DIR))
print(f"[INFO] - append directory to path: {PROJECT_DIR}")

import time
import random
from src.tinder import TinderAPI
from pprint import pp

token = ''
tinder_api = TinderAPI(token)


def main():
    girl_idx = 0
    flag = True
    while flag:
        recs_user_ls = tinder_api.get_recommendations()
        for recs_user in recs_user_ls:
            if recs_user.is_girl:
                res = recs_user.like_her()
                girl_idx += 1
                msg = f"({str(girl_idx).zfill(3)}) liked {recs_user}, dist: {recs_user.distance_km}, " \
                      f"status: {res.get('status')}, " \
                      f"match: {res.get('match')}, " \
                      f"like: {res.get('likes_remaining')}"
                print(msg)

                wait_sec_ls = [3, 6]
                time.sleep(random.choice(wait_sec_ls))

                if res['status'] != 200:
                    flag = False

        time.sleep(60)


if __name__ == '__main__':
    main()
