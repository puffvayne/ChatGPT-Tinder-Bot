import re
from .ChatGPTAPI import ChatGPT


def predict_hook_up_intention(prompt, chat_gpt_token) -> float:
    chat_gpt = ChatGPT(token=chat_gpt_token)
    response = chat_gpt(prompt)
    # print(response)

    numeric_vals = re.findall(r'\d+\.?\d*', response)
    value = float(numeric_vals[0]) if numeric_vals else 1.0
    return value
