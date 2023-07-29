import pathlib
import sys

# add project directory to path
curr_file_path = pathlib.Path(__file__).absolute()
CURR_DIR = curr_file_path.parent
PROJECT_DIR = CURR_DIR.parent
sys.path.append(str(PROJECT_DIR))
print(f"[INFO] - append directory to path: {PROJECT_DIR}")

from tinder_bot.models import OpenAIModel
from tinder_bot.chatgpt import ChatGPT

OPENAI_API = 'sk-'
OPENAI_MODEL_ENGINE = 'gpt-3.5-turbo'
models = OpenAIModel(api_key=OPENAI_API, model_engine=OPENAI_MODEL_ENGINE)
chatgpt = ChatGPT(models)
response = chatgpt.get_response('explain about large language model')
print(response)
