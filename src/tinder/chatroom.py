from typing import List
from .message import Message
from typing import Dict


class PlainChatroom:
    def __init__(self, data: Dict, match_id: str, api):
        from .tinder_api import TinderAPI
        self._api: TinderAPI = api
        self.match_id = match_id
        self.messages: List[Message] = list(
            map(
                lambda message: Message(match_id, message, self), data['messages']
            )
        )

    def send(self, message, from_id, to_id):
        return self._api.send_message(self.match_id, from_id, to_id, message)

    def get_latest_message(self):
        if len(self.messages) > 0:
            return self.messages[0]
        return None

    def __repr__(self) -> str:
        s = f"PlainChatroom: {self.match_id}"
        return s


class Chatroom(PlainChatroom):
    def __init__(self, data: Dict, match, api):
        from .match import Match
        from .tinder_api import TinderAPI
        match: Match
        api: TinderAPI
        super().__init__(data, match.match_id, api)
        self.person = match.person

    def __repr__(self) -> str:
        s = f"Chatroom: {self.match_id} with {self.person}"
        return s
