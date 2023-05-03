import time

import requests
import random
from typing import Union, List, Dict
from . import TINDER_URL, ASK_HOOK_UP_MSG_LS


class TinderAPI:
    def __init__(self, token):
        self._token = token
        self._headers = {
            'X-Auth-Token': self._token
        }
        self.chatroom_match_id_ls = list()
        profile = self.profile()
        self.user_name = profile.name
        self.user_id = profile.id

    def __repr__(self) -> str:
        s = f"TinderAPI : {self.user_id} - {self.user_name}"
        return s

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

    def get_matches(self, limit=60) -> List:
        from .match import Match
        url = TINDER_URL + f"/v2/matches?count={limit}"
        data = requests.get(url, headers=self._headers).json()
        self.chatroom_match_id_ls = list(map(lambda match: match['id'], data['data']['matches']))
        return list(map(lambda match: Match(match, self), data['data']['matches']))

    def get_msg_data_with_match_id(self, match_id: str) -> Dict:
        url = TINDER_URL + f"/v2/matches/{match_id}/messages?count=90"
        msg_data = requests.get(url, headers=self._headers).json()
        return msg_data

    def get_plain_chatroom(self, match_id):
        from .chatroom import PlainChatroom
        msg_data = self.get_msg_data_with_match_id(match_id)
        return PlainChatroom(msg_data['data'], match_id, self)

    def get_chatroom(self, match):
        from .match import Match
        from .chatroom import Chatroom
        match: Match
        msg_data = self.get_msg_data_with_match_id(match.match_id)
        return Chatroom(msg_data['data'], match, self)

    def get_user_info(self, user_id):
        from .person import Person
        url = TINDER_URL + f"/user/{user_id}"
        data = requests.get(url, headers=self._headers).json()
        if data['status'] == 200:
            return Person(data['results'], self)
        else:
            msg = f"server response != 200, when getting user info"
            print(msg)
        # return PlainPerson(data["results"], self)

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

    def super_like(self, user_id) -> Dict:
        try:
            url = TINDER_URL + f"/like/{user_id}/super"
            response = requests.post(url, headers=self._headers)
            return response.json()
        except requests.exceptions.RequestException as e:
            msg = f"failed to super like a girl, Error: {e}"
            print(msg)

    def like(self, user_id) -> Dict:
        try:
            url = TINDER_URL + f"/like/{user_id}"
            response = requests.get(url, headers=self._headers)
            return response.json()
        except requests.exceptions.RequestException as e:
            msg = f"failed to like a girl, Error: {e}"
            print(msg)

    def swipe_left(self, user_id) -> Dict:
        try:
            url = TINDER_URL + f"/pass/{user_id}"
            response = requests.get(url, headers=self._headers)
            return response.json()
        except requests.exceptions.RequestException as e:
            msg = f"failed to pass a girl, Error: {e}"
            print(msg)

    def ask_hook_up(self, chatroom):
        from .chatroom import Chatroom
        chatroom: Chatroom
        greet_line_ls = random.choice(ASK_HOOK_UP_MSG_LS)
        for greet_idx, greet_line in enumerate(greet_line_ls):
            msg_sent_response = chatroom.send(self.user_id, chatroom.person.id, greet_line)
            print(f"msg_sent_response:\n{msg_sent_response}\n")

            if greet_idx == 0:
                time.sleep(random.uniform(.5, 1))
            else:
                time.sleep(random.uniform(3, 6))

    def dev_query(self):
        limit = 60
        url = TINDER_URL + f"/v2/matches?count={limit}"
        data = requests.get(url, headers=self._headers).json()
        return data

    def get_user_info_json(self, user_id: str):
        url = TINDER_URL + f"/user/{user_id}"
        data = requests.get(url, headers=self._headers).json()
        return data

    def unmatch(self, match_id: str) -> Dict:
        from .match import Match
        if isinstance(match_id, Match):
            match_id = match_id.match_id
        url = TINDER_URL + f"/user/matches/{match_id}"
        data = requests.delete(url, headers=self._headers).json()
        return data

    def ping(self, lat: float = 25.08402660022195, lon: float = 121.56159729461773):
        url = TINDER_URL + '/user/ping'
        body = {
            'lat': lat,
            'lon': lon,
        }
        data = requests.post(url, json=body, headers=self._headers).json()
        return data
