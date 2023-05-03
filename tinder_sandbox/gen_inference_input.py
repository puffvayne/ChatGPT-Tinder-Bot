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

for match in tinder_api.get_matches(60):
    # if match.person.name != 'Mary':
    #     continue
    chatroom = tinder_api.get_chatroom(match)
    # print(f"has asked for hk = {chatroom.has_asked_hook_up}, has reply hk = {chatroom.has_replied_about_hook_up}, {chatroom}")
    if chatroom.has_replied_about_hook_up:
        print(chatroom.gen_hook_up_intention_inference_prompt())
