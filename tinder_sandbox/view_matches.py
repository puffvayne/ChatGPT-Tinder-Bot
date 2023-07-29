import json
import pathlib
import sys

# add project directory to path
curr_file_path = pathlib.Path(__file__).absolute()
CURR_DIR = curr_file_path.parent
PROJECT_DIR = CURR_DIR.parent
sys.path.append(str(PROJECT_DIR))
print(f"[INFO] - append directory to path: {PROJECT_DIR}")

from tinder_bot.tinder import TinderAPI, Person
from tinder_bot.utils import to_json, read_json

token = ''
tinder_api = TinderAPI(token)
print(tinder_api)
from pprint import pp

for match in tinder_api.get_matches(60):
    if match.person.name != 'Era':
        continue
    chatroom = tinder_api.get_chatroom(match)
    print(match.person.name)
    msg = f"has asked for hk = {chatroom.has_asked_hook_up}, " \
          f"has reply hk = {chatroom.has_replied_about_hook_up}, " \
          f"has ensured girls reply = {chatroom.has_ensured_girls_reply}, " \
          f"{chatroom}"
    print(msg)
    user = tinder_api.get_user_info(match.person.id)
    pp(user.infos())
    unmatch_resp = match.unmatch_her()
    print(unmatch_resp)

    # if chatroom.has_replied_about_hook_up:
    #     print(chatroom.gen_hook_up_intention_inference_prompt())
