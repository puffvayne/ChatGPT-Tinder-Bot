from .person import Person


class Match:
    def __init__(self, data, api):
        from .tinder_api import TinderAPI
        api: TinderAPI
        self.match_id = data['id']
        self.person = Person(data['person'], api)

    def __repr__(self) -> str:
        s = f"Match: {self.match_id} with {self.person}"
        return s
