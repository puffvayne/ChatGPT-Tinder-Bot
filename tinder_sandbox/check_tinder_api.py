import pathlib
import sys

# add project directory to path
curr_file_path = pathlib.Path(__file__).absolute()
CURR_DIR = curr_file_path.parent
PROJECT_DIR = CURR_DIR.parent
sys.path.append(str(PROJECT_DIR))
print(f"[INFO] - append directory to path: {PROJECT_DIR}")

from src.tinder import TinderAPI, ASK_HOOK_UP_MSG_LS

token = ''
tinder_api = TinderAPI(token)
print(tinder_api)

print(tinder_api.profile())

rec_ls = tinder_api.get_recommendations()
print(rec_ls)
print(f"rec_ls len = {len(rec_ls)}")

match_ls = tinder_api.get_matches()
print(match_ls)

match = match_ls[0]
print(match)

plain_chatroom = tinder_api.get_plain_chatroom(match.match_id)
print(plain_chatroom)

chatroom = tinder_api.get_chatroom(match)
print(chatroom)

print(ASK_HOOK_UP_MSG_LS)
