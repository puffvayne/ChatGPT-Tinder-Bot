import datetime
from typing import Dict


class RecPerson:
    GENDER_DICT = {
        0: 'Male',
        1: 'Female',
        -1: 'Unknown',
    }

    UNWANTED_SO_LS = [
        'Asexual',
        'Gay',
        'Lesbian',
    ]

    UNWANTED_KW_LS = [
        'gay',
        '同性',
        'lady boy',
        'transsexual',
        '變性',
    ]

    def __init__(self, data: Dict, api):
        """
        parsed data from https://api.gotinder.com/v2/recs/core

        :param data: Dict
        :param api: TinderAPI
        """
        from .tinder_api import TinderAPI
        assert isinstance(api, TinderAPI)
        self._api: TinderAPI = api

        user_data = data['user']
        self.id = user_data['_id']
        self.name = user_data.get('name', 'Unknown')
        self.gender = self.GENDER_DICT[user_data.get('gender', -1)]

        sexual_orientations = user_data.get('sexual_orientations', list())
        self.sexual_orientations = [so.get('name') for so in sexual_orientations]

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

        self.images = list(map(lambda photo: photo['url'], user_data.get('photos', list())))

        self.distance_mile = data.get('distance_mi', -1)
        self.distance_km = round(self.distance_mile * 1.609344, 3) if self.distance_mile != -1 else -1

    def __repr__(self) -> str:
        if self.birth_date == 'Unknown':
            birth_date_str = self.birth_date
        else:
            birth_date_str = self.birth_date.strftime('%Y.%m.%d')
        s = f"RecPerson: {self.id} - {self.name} ({self.gender}) ({self.city}, {int(round(self.distance_km))} km) ({birth_date_str})"

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

    @property
    def is_valid_so(self) -> bool:
        if len(self.sexual_orientations) == 0:
            return False

        for unwanted_so in self.UNWANTED_SO_LS:
            if unwanted_so in self.sexual_orientations:
                return False

        return True

    @property
    def is_near(self) -> bool:
        if self.distance_km < 30:
            return True
        else:
            return False

    @property
    def is_unwanted(self) -> bool:
        if not self.is_near:
            return True

        about_str: str = self.name + self.bio
        about_str = about_str.lower()

        for uw_kw in self.UNWANTED_KW_LS:
            if uw_kw in about_str:
                return True

        for un_so in self.UNWANTED_SO_LS:
            if un_so in self.sexual_orientations:
                return True

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

    def super_like_her(self) -> Dict:
        return self._api.super_like(self.id)

    def like_her(self) -> Dict:
        return self._api.like(self.id)

    def swipe_her_left(self) -> Dict:
        return self._api.swipe_left(self.id)
