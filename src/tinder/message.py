import datetime


class Message:
    def __init__(self, match_id, data, api):
        from .tinder_api import TinderAPI
        self._api: TinderAPI = api
        self.match_id = match_id
        self.message_id = data['_id']
        self.sent_date = data['sent_date']
        self.message = data['message']
        self.to_id = data['to']
        self.from_id = data['from']
        self.sent_date = datetime.datetime.strptime(data['sent_date'], '%Y-%m-%dT%H:%M:%S.%fZ')

    def __repr__(self):
        return f"{self.from_id}: {self.message}"
