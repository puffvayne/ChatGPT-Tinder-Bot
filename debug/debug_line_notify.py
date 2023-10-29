import pathlib
import sys

# add project directory to path
curr_file_path = pathlib.Path(__file__).absolute()
CURR_DIR = curr_file_path.parent
PROJECT_DIR = CURR_DIR.parent
sys.path.append(str(PROJECT_DIR))
print(f"[INFO] - append directory to path: {PROJECT_DIR}")

from tinder_bot.utils import var as VAR
from tinder_bot.utils.log_tool import get_cls_instance_logger
from tinder_bot.utils.notify_tool.line.tool import send_message_by_line_notify

send_message_by_line_notify('xxx')
