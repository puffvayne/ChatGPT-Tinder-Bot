from .pyChatGPT import ChatGPT as Chatbot

import requests
from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Any
import pydantic
import os
from langchain import PromptTemplate, LLMChain
from time import sleep


class ChatGPT(LLM):
    history_data: Optional[List] = []
    token: Optional[str]
    chatbot: Optional[Chatbot] = None
    call: int = 0
    conversation: Optional[str] = ""

    #### WARNING : for each api call this library will create a new chat on chat.openai.com

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")
        # token is a must check
        if self.chatbot is None:
            if self.token is None:
                raise ValueError("Need a token , check https://chat.openai.com/api/auth/session for get your token")
            else:
                if self.conversation == "":
                    self.chatbot = Chatbot(self.token)
                elif self.conversation != "":
                    self.chatbot = Chatbot(self.token, conversation_id=self.conversation)
                else:
                    raise ValueError("Something went wrong")

        response = ""
        # OpenAI: 50 requests / hour for each account
        if self.call >= 45:
            raise ValueError(
                "You have reached the maximum number of requests per hour ! Help me to Improve. Abusing this tool is at your own risk")
        else:
            sleep(2)
            data = self.chatbot.send_message(prompt)
            # print(data)
            response = data["message"]
            self.conversation = data["conversation_id"]
            FullResponse = data

            self.chatbot.clear_conversations()

            self.call += 1

        # add to history
        self.history_data.append({"prompt": prompt, "response": response})

        return response

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"model": "ChatGPT", "token": self.token}

# llm = ChatGPT(token = "YOUR-COOKIE") #for start new chat

# llm = ChatGPT(token = "YOUR-COOKIE", conversation = "Add-XXXX-XXXX-Convesation-ID") #for use a chat already started

# print(llm("Hello, how are you?"))
# print(llm("what is AI?"))
# print(llm("Can you resume your previus answer?")) #now memory work well
