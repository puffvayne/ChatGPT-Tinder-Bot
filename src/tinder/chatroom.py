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

    def print_messages(self):
        for msg in self.messages:
            print(msg)


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

    def get_hook_up_asking_conversation(self) -> Dict:
        key_line_msg_idx = None
        msg_old_to_new = list(reversed(self.messages))
        for msg_idx, msg in enumerate(msg_old_to_new):
            if msg.is_ask_hook_up_key_line:
                key_line_msg_idx = msg_idx

        my_asking_msg_ls = [msg_old_to_new[key_line_msg_idx]]
        for msg_idx in range(key_line_msg_idx - 1, -1, -1):
            msg = msg_old_to_new[msg_idx]
            if msg.is_from_me:
                my_asking_msg_ls.insert(0, msg)

        other_reply_msg_st_idx = None
        for msg_idx in range(key_line_msg_idx + 1, len(msg_old_to_new)):
            msg = msg_old_to_new[msg_idx]
            if msg.is_from_me:
                my_asking_msg_ls.append(msg)
            else:
                other_reply_msg_st_idx = msg_idx
                break

        other_reply_msg_ls = list()
        for msg_idx in range(other_reply_msg_st_idx, len(msg_old_to_new)):
            msg = msg_old_to_new[msg_idx]
            if msg.is_from_other:
                other_reply_msg_ls.append(msg)
            else:
                break

        # print(my_asking_msg_ls)
        # print(other_reply_msg_ls)

        return {'me': my_asking_msg_ls, 'other': other_reply_msg_ls}

    def gen_hook_up_intention_inference_prompt(self) -> str:
        hook_up_conv_dict = self.get_hook_up_asking_conversation()
        my_asking = str([my_asking_msg.message for my_asking_msg in hook_up_conv_dict['me']])
        other_reply = str([other_reply_msg.message for other_reply_msg in hook_up_conv_dict['other']])
        prompt = f"我要你扮演一個計算女方赴約意願的計算機," \
                 f"你的回答只能是 decimal with 1 digit from 0.0 to 10.0, 0.0 is the min and 10.0 is the max," \
                 f"女方的意願的最低值為 0.0,意願最高為 10.0,若你認為女方沒有任何明顯的傾向,請計算為5.0," \
                 f"我會給你一段關於一對男女的對話,請你嘗試理解對話內容並計算女方的附約意願。" \
                 f"以下為對話內容 -> 男方 : {my_asking}, 女方: {other_reply}。" \
                 f"注意:你無須回答我任何你對於對話的理解,你只能回答我數值,因為你的回答將作為python代碼的input,ex:float(你的回答)"

        return prompt

    @property
    def has_asked_hook_up(self) -> bool:
        if len(self.messages) == 0:
            return False

        if self.has_talked_awhile:
            return True

        for msg in reversed(self.messages):
            if msg.is_from_me and msg.message == ASK_HOOK_UP_KEY_LINE:
                return True

        return False

    @property
    def has_talked_awhile(self) -> bool:
        if len(self.messages) > 30:
            return True
        else:
            return False

    @property
    def has_replied_about_hook_up(self) -> bool:
        if not self.has_asked_hook_up:
            return False

        if self.has_talked_awhile:
            return True

        key_line_msg_idx = None
        msg_old_to_new = list(reversed(self.messages))
        for msg_idx, msg in enumerate(msg_old_to_new):
            if msg.is_ask_hook_up_key_line:
                key_line_msg_idx = msg_idx

        for msg_idx in range(key_line_msg_idx + 1, len(msg_old_to_new)):
            msg = msg_old_to_new[msg_idx]
            if msg.is_from_other:
                first_reply_msg = msg
                # print(f"first_reply_msg = {first_reply_msg}")
                return True

        return False

    @property
    def has_ensured_girls_reply(self) -> bool:
        if not self.has_replied_about_hook_up:
            return False

        if self.has_talked_awhile:
            return True

        key_line_msg_idx = None
        msg_old_to_new = list(reversed(self.messages))
        for msg_idx, msg in enumerate(msg_old_to_new):
            if msg.is_ask_hook_up_key_line:
                key_line_msg_idx = msg_idx

        my_asking_msg_ls = [msg_old_to_new[key_line_msg_idx]]
        for msg_idx in range(key_line_msg_idx - 1, -1, -1):
            msg = msg_old_to_new[msg_idx]
            if msg.is_from_me:
                my_asking_msg_ls.insert(0, msg)

        other_reply_msg_st_idx = None
        for msg_idx in range(key_line_msg_idx + 1, len(msg_old_to_new)):
            msg = msg_old_to_new[msg_idx]
            if msg.is_from_me:
                my_asking_msg_ls.append(msg)
            else:
                other_reply_msg_st_idx = msg_idx
                break

        for msg_idx in range(other_reply_msg_st_idx + 1, len(msg_old_to_new)):
            msg = msg_old_to_new[msg_idx]
            if msg.is_from_me:
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
