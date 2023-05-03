import pathlib
import sys

# add project directory to path
curr_file_path = pathlib.Path(__file__).absolute()
CURR_DIR = curr_file_path.parent
PROJECT_DIR = CURR_DIR.parent
sys.path.append(str(PROJECT_DIR))
print(f"[INFO] - append directory to path: {PROJECT_DIR}")

from src.LLM import predict_hook_up_intention
from src.tinder import TinderAPI

gpt_token = open('cookies.txt', 'r').read()
# llm = ChatGPT(token=token)  # for start new chat

token = ''
tinder_api = TinderAPI(token)
print(tinder_api)

for match in tinder_api.get_matches(60):
    # if match.person.name != 'Mary':
    #     continue
    chatroom = tinder_api.get_chatroom(match)
    # print(f"has asked for hk = {chatroom.has_asked_hook_up}, has reply hk = {chatroom.has_replied_about_hook_up}, {chatroom}")
    if chatroom.has_replied_about_hook_up:
        prompt = chatroom.gen_hook_up_intention_inference_prompt()
        response = predict_hook_up_intention(prompt, gpt_token)
        print(response)
