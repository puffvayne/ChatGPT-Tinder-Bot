import pathlib
import sys

# add project directory to path
curr_file_path = pathlib.Path(__file__).absolute()
CURR_DIR = curr_file_path.parent
PROJECT_DIR = CURR_DIR.parent
sys.path.append(str(PROJECT_DIR))
print(f"[INFO] - append directory to path: {PROJECT_DIR}")

from tinder_bot.models import OpenAIModel
from tinder_bot.chatgpt import ChatGPT, DALLE
import openai
from pprint import pp


def list_all_models(api_key):
    openai.api_key = api_key
    model_list = openai.Model.list()['data']
    model_ids = [x['id'] for x in model_list]
    model_ids.sort()
    pp(model_ids)


OPENAI_API = ''
list_all_models(OPENAI_API)
