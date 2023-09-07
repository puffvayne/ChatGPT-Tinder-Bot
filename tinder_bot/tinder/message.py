import datetime
from . import ASK_HOOK_UP_KEY_LINE_LS


class Message:
    def __init__(self, match_id, data, api):
        from .tinder_api import TinderAPI
        assert isinstance(api, TinderAPI)
        self._api: TinderAPI = api
        self.match_id = match_id
        self.message_id = data['_id']
        self.sent_date = data['sent_date']
        self.message = data['message']
        self.to_id = data['to']
        self.from_id = data['from']
        self.sent_date = datetime.datetime.strptime(data['sent_date'], '%Y-%m-%dT%H:%M:%S.%fZ')

    def __repr__(self) -> str:
        if self.is_from_me:
            speaker = f"*******Me ({self._api.user_name})*******"
        else:
            speaker = f"{self.from_id}"

        s = f"MSG: {self.sent_date.strftime('%Y-%m-%d %H:%M:%S')} - {speaker}: {self.message}"
        return s

    @property
    def is_from_me(self) -> bool:
        if self.from_id == self._api.user_id:
            return True
        else:
            return False

    @property
    def is_from_other(self) -> bool:
        if not self.is_from_me:
            return True
        else:
            return False

    @property
    def is_ask_hook_up_key_line(self) -> bool:
        if self.is_from_me and self.message in ASK_HOOK_UP_KEY_LINE_LS:
            return True
        else:
            return False
