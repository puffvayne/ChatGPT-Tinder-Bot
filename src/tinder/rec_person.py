import datetime
from typing import Dict


class RecPerson:
    GENDER_DICT = {
        0: 'Male',
        1: 'Female',
        -1: 'Unknown',
    }

    def __init__(self, data: Dict, api):
        """
        parsed data from https://api.gotinder.com/v2/recs/core

        :param data: Dict
        :param api: TinderAPI
        """
        from .tinder_api import TinderAPI
        self._api: TinderAPI = api

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
        self.birth_date = datetime.datetime.strptime(user_data['birth_date'], '%Y-%m-%dT%H:%M:%S.%fZ') if user_data.get(
            'birth_date', False) else 'Unknown'
        self.city = user_data.get('city', dict()).get('name', 'Unknown')
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
                lambda job: {
                    'title': job.get('title', dict()).get('name'),
                    'company': job.get('company', dict()).get('name')}, user_data.get('jobs', list())
            )
        )
        self.schools = list(map(lambda school: school['name'], user_data.get('schools', list())))

        self.distance_mile = data.get('distance_mi', -1)
        self.distance_km = round(self.distance_mile * 1.609344, 3) if self.distance_mile != -1 else -1

    def __repr__(self) -> str:
        if self.birth_date == 'Unknown':
            birth_date_str = self.birth_date
        else:
            birth_date_str = self.birth_date.strftime('%Y.%m.%d')
        s = f"RecPerson: {self.id} - {self.name} ({self.city}, {int(round(self.distance_km))} km) ({birth_date_str})"

        return s

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
