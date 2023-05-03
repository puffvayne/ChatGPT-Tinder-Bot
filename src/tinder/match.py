from typing import Dict
from .person import PlainPerson


class Match:
    def __init__(self, data, api):
        from .tinder_api import TinderAPI
        assert isinstance(api, TinderAPI)
        api: TinderAPI
        self._api = api
        self.match_id = data['id']
        self.person = PlainPerson(data['person'], api)

    def __repr__(self) -> str:
        s = f"Match: {self.match_id} with {self.person}"
        return s

    def unmatch_her(self) -> Dict:
        return self._api.unmatch(self.match_id)
