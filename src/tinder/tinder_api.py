import requests
from typing import Union, List, Dict
from . import TINDER_URL


class TinderAPI:
    def __init__(self, token):
        self._token = token
        self._headers = {
            'X-Auth-Token': self._token
        }
        self.chatroom_match_id = list()

    def profile(self):
        from .profile import Profile
        url = TINDER_URL + "/v2/profile?include=account%2Cuser"
        data = requests.get(url, headers=self._headers).json()
        return Profile(data["data"], self)

    def get_recommendations(self):
        from .rec_person import RecPerson
        try:
            url = TINDER_URL + '/v2/recs/core'
            response = requests.get(url, headers=self._headers)
            rec_user_ls = list()
            data = response.json()
            if data['meta']['status'] != 200:
                msg = f"server response != 200, when getting recommendations"
                print(msg)
                return rec_user_ls

            for d in data['data']['results']:
                if d['type'] == 'user':
                    rec_user_ls.append(RecPerson(d, self))
            return rec_user_ls
        except requests.exceptions.RequestException as e:
            msg = f"failed to get recommendations, Error: {e}"
            print(msg)

    def get_recommendations_v1(self):
        try:
            url = TINDER_URL + '/user/recs'
            response = requests.get(url, headers=self._headers)
            return response.json()
        except requests.exceptions.RequestException as e:
            msg = f"failed to get recommendations_v1, Error: {e}"
            print(msg)

    def get_matches(self, limit=15) -> List:
        from .match import Match
        url = TINDER_URL + f"/v2/matches?count={limit}"
        data = requests.get(url, headers=self._headers).json()
        self.chatroom_match_id = list(map(lambda match: match['id'], data['data']['matches']))
        return list(map(lambda match: Match(match, self), data['data']['matches']))

    def _get_msg_data_with_match_id(self, match_id: str) -> Dict:
        url = TINDER_URL + f"/v2/matches/{match_id}/messages?count=50"
        msg_data = requests.get(url, headers=self._headers).json()
        return msg_data

    def get_plain_chatroom(self, match_id):
        from .chatroom import PlainChatroom
        msg_data = self._get_msg_data_with_match_id(match_id)
        return PlainChatroom(msg_data['data'], match_id, self)

    def get_chatroom(self, match):
        from .match import Match
        from .chatroom import Chatroom
        match: Match
        msg_data = self._get_msg_data_with_match_id(match.match_id)
        return Chatroom(msg_data['data'], match, self)

    def get_user_info(self, user_id):
        from .person import Person
        url = TINDER_URL + f"/user/{user_id}"
        data = requests.get(url, headers=self._headers).json()
        return Person(data["results"], self)

    def send_message(self, match_id, from_id, to_id, message):
        body = {
            'matchId': match_id,
            'message': message,
            'userId': from_id,
            'otherId': to_id,
            'sessonId': None
        }
        url = TINDER_URL + f'/user/matches/{match_id}'
        data = requests.post(url, json=body, headers=self._headers).json()
        return data

    def like(self, user_id) -> Dict:
        try:
            url = TINDER_URL + f"/like/{user_id}"
            response = requests.get(url, headers=self._headers)
            return response.json()
        except requests.exceptions.RequestException as e:
            msg = f"failed to like a girl, Error: {e}"
            print(msg)

    def meta(self):
        try:
            url = TINDER_URL + '/v2/meta'
            response = requests.get(url, headers=self._headers)
            return response.json()
        except requests.exceptions.RequestException as e:
            msg = f"failed to get meta, Error: {e}"
            print(msg)

    def meta_v1(self):
        try:
            url = TINDER_URL + '/meta'
            response = requests.get(url, headers=self._headers)
            return response.json()
        except requests.exceptions.RequestException as e:
            msg = f"failed to get meta v1, Error: {e}"
            print(msg)

    def get_remaining_likes(self):
        try:
            meta_v1 = self.meta_v1()
            return meta_v1.get('rating', dict()).get('likes_remaining', 0)
        except requests.exceptions.RequestException as e:
            msg = f"failed to get remaining likes, Error: {e}"
            print(msg)
