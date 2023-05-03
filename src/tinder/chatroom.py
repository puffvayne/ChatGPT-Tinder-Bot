from typing import List, Union
from .message import Message
from typing import Dict
from . import ASK_HOOK_UP_KEY_LINE


class PlainChatroom:
    def __init__(self, data: Dict, match_id: str, api):
        from .tinder_api import TinderAPI
        assert isinstance(api, TinderAPI)
        self._api: TinderAPI = api
        self.match_id = match_id
        self.messages: List[Message] = list(
            map(
                lambda message: Message(match_id, message, self._api), data['messages']
            )
        )

    def send(self, from_id, to_id, message):
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
        assert isinstance(api, TinderAPI)
        super().__init__(data, match.match_id, api)
        self.person = match.person

    def __repr__(self) -> str:
        s = f"Chatroom: {self.match_id} with {self.person}"
        return s

    @property
    def has_asked_hook_up(self) -> bool:
        if len(self.messages) == 0:
            return False

        for msg in reversed(self.messages):
            if msg.from_id == self._api.user_id and msg.message == ASK_HOOK_UP_KEY_LINE:
                return True

        return False

    @property
    def has_replied_about_hook_up(self) -> bool:
        if not self.has_asked_hook_up:
            return False

        key_line_msg_idx = None
        msg_old_to_new = list(reversed(self.messages))
        for i, msg in enumerate(msg_old_to_new):
            if msg.is_ask_hook_up_key_line:
                key_line_msg_idx = i

        for msg_idx in range(key_line_msg_idx + 1, len(self.messages)):
            msg = msg_old_to_new[msg_idx]
            if msg.is_from_other:
                first_reply_msg = msg
                # print(f"first_reply_msg = {first_reply_msg}")
                return True

        return False

    @property
    def last_replied_person(self) -> Union[str, None]:
        latest_msg = self.get_latest_message()
        if latest_msg is None:
            return None

        if latest_msg.from_id == self._api.user_id:
            return 'me'
        else:
            return 'other'

    @property
    def is_my_turn(self) -> bool:
        if self.last_replied_person == 'me':
            return False
        else:
            return True
