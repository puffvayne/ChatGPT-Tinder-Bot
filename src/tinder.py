from typing import Dict, Union
import requests
import datetime

TINDER_URL = "https://api.gotinder.com"


class TinderAPI:
    def __init__(self, token):
        self._token = token
        self._headers = {
            'X-Auth-Token': self._token
        }
        self.chatroom_match_id = list()

    def profile(self):
        url = TINDER_URL + "/v2/profile?include=account%2Cuser"
        data = requests.get(url, headers=self._headers).json()
        return Profile(data["data"], self)

    def get_recommendations(self):
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

    def matches(self, limit=10):
        url = TINDER_URL + f"/v2/matches?count={limit}"
        data = requests.get(url, headers=self._headers).json()
        self.chatroom_match_id = list(map(lambda match: match['id'], data["data"]["matches"]))
        return list(map(lambda match: Match(match, self), data["data"]["matches"]))

    def get_messages(self, match_id):
        url = TINDER_URL + f"/v2/matches/{match_id}/messages?count=50"
        data = requests.get(url, headers=self._headers).json()
        return Chatroom(data['data'], match_id, self)

    def get_user_info(self, user_id):
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


class Chatroom(object):
    def __init__(self, data, match_id, api):
        self._api = api
        self.match_id = match_id
        self.messages = list(map(lambda message: Message(match_id, message, self), data['messages']))

    def send(self, message, from_id, to_id):
        return self._api.send_message(self.match_id, from_id, to_id, message)

    def get_lastest_message(self):
        if len(self.messages) > 0:
            return self.messages[0]
        return None


class Message(object):
    def __init__(self, match_id, data, api):
        self._api = api
        self.match_id = match_id
        self.message_id = data['_id']
        self.sent_date = data['sent_date']
        self.message = data['message']
        self.to_id = data['to']
        self.from_id = data['from']
        self.sent_date = datetime.datetime.strptime(data['sent_date'], '%Y-%m-%dT%H:%M:%S.%fZ')

    def __repr__(self):
        return f'{self.from_id}: {self.message}'


class Match(object):
    def __init__(self, data, api):
        self.match_id = data['id']
        self.person = Person(data['person'], api)


class Person(object):

    def __init__(self, data, api):
        self._api = api

        self.id = data["_id"]

        self.name = data.get("name", "Unknown")

        self.bio = data.get("bio", "")
        self.city = data.get("city", dict()).get('name', "")
        self.relationship_intent = data.get("relationship_intent", dict()).get('body_text', "")
        selected_descriptors = data.get('selected_descriptors', list())
        self.selected_descriptors = list()
        for selected_descriptor in selected_descriptors:
            if selected_descriptor.get('prompt'):
                self.selected_descriptors.append(
                    f"{selected_descriptor.get('prompt')} {'/'.join([s['name'] for s in selected_descriptor['choice_selections']])}")
            else:
                self.selected_descriptors.append(
                    f"{selected_descriptor.get('name')}: {'/'.join([s['name'] for s in selected_descriptor['choice_selections']])}")

        self.distance = data.get("distance_mi", 0) / 1.60934

        self.birth_date = datetime.datetime.strptime(data["birth_date"], '%Y-%m-%dT%H:%M:%S.%fZ') if data.get(
            "birth_date", False) else None
        self.gender = ["Male", "Female", "Unknown"][data.get("gender", 2)]

        self.images = list(map(lambda photo: photo["url"], data.get("photos", list())))

        self.jobs = list(
            map(lambda job: {"title": job.get("title", dict()).get("name"),
                             "company": job.get("company", dict()).get("name")},
                data.get("jobs", list())))
        self.schools = list(map(lambda school: school["name"], data.get("schools", list())))

    def infos(self):
        return {
            'name': self.name,
            'bio': self.bio,
            'city': self.city,
            'relationship_intent': self.relationship_intent,
            'selected_descriptors': self.selected_descriptors,
            'birth_date': self.birth_date,
            'gender': self.gender,
            'jobs': self.jobs,
            'schools': self.schools
        }

    def __repr__(self):
        return f"{self.id} - {self.name} ({self.birth_date.strftime('%d.%m.%Y')})"


class RecPerson:
    GENDER_DICT = {
        0: 'Male',
        1: 'Female',
        -1: 'Unknown',
    }

    def __init__(self, data: Dict, api: TinderAPI):
        self._api = api

        user_data = data['user']
        self.id = user_data['_id']
        self.name = user_data.get('name', 'Unknown')
        self.gender = self.GENDER_DICT[user_data.get('gender', -1)]
        self.badges = user_data.get('badges', list())
        self.selfie_verified = False
        for badges in self.badges:
            if badges.get('type', '') == 'selfie_verified':
                self.selfie_verified = True

        self.bio = user_data.get('bio', '')
        self.birth_date = datetime.datetime.strptime(user_data["birth_date"], '%Y-%m-%dT%H:%M:%S.%fZ') if user_data.get(
            'birth_date', False) else None
        self.city = user_data.get('city', dict()).get('name', '')
        self.relationship_intent = user_data.get('relationship_intent', dict()).get('body_text', '')

        selected_descriptors = user_data.get('selected_descriptors', list())
        self.selected_descriptors = dict()
        for sel_desc in selected_descriptors:
            section_name = sel_desc.get('section_name', None)
            choice_selections = [choice.get('name', '') for choice in sel_desc.get('choice_selections', list())]
            if section_name and len(choice_selections):
                if section_name in self.selected_descriptors.keys():
                    self.selected_descriptors[section_name].extend(choice_selections)
                else:
                    self.selected_descriptors[section_name] = choice_selections

        self.jobs = list(
            map(
                lambda job: {"title": job.get("title", dict()).get("name"),
                             "company": job.get("company", dict()).get("name")},
                user_data.get("jobs", list())
            )
        )
        self.schools = list(map(lambda school: school["name"], user_data.get("schools", list())))

        self.distance_mile = data.get('distance_mi', -1)
        self.distance_km = round(self.distance_mile * 1.609344, 3) if self.distance_mile != -1 else -1

    def __repr__(self):
        return f"{self.id} - {self.name} ({self.birth_date.strftime('%d.%m.%Y')})"

    @property
    def is_girl(self) -> bool:
        if self.gender == 'Female':
            return True
        else:
            return False

    @property
    def is_verified_girl(self) -> bool:
        if self.is_girl and self.selfie_verified:
            return True
        else:
            return False

    def info(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'badges': self.badges,
            'selfie_verified': self.selfie_verified,
            'bio': self.bio,
            'birth_date': self.birth_date,
            'city': self.city,
            'relationship_intent': self.relationship_intent,
            'selected_descriptors': self.selected_descriptors,
            'jobs': self.jobs,
            'schools': self.schools,
            'distance_mile': self.distance_mile,
            'distance_km': self.distance_km,
        }

    def like_her(self) -> Dict:
        return self._api.like(self.id)


class Profile(Person):

    def __init__(self, data, api):
        super().__init__(data["user"], api)
        self.email = data["account"].get("email")
        self.phone_number = data["account"].get("account_phone_number")

        self.age_min = data["user"]["age_filter_min"]
        self.age_max = data["user"]["age_filter_max"]
        user_interests = data["user"].get('user_interests', dict()).get('selected_interests', list())
        self.user_interests = list()
        for user_interest in user_interests:
            self.user_interests.append(user_interest.get('name'))

        self.max_distance = data["user"]["distance_filter"]
        self.gender_filter = ["Male", "Female"][data["user"]["gender_filter"]]
